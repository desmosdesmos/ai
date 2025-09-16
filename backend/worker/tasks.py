import os
import pandas as pd
from . import celery_app
from ..app.config import get_settings
from ..app.db import SessionLocal
from ..app.models.models import ProcessingJob
from ..app.services.rules_service import find_rule
from ..app.utils.normalization import (
	normalize_article,
	normalize_part,
	normalize_point,
	normalize_amount,
	map_rekvizit_code,
)


@celery_app.task(name="backend.worker.tasks.process_excel_job")
def process_excel_job(job_id: str):
	settings = get_settings()
	db = SessionLocal()
	try:
		job = db.get(ProcessingJob, job_id)
		if not job:
			return
		job.status = "processing"
		db.commit()

		# Read input Excel
		df = pd.read_excel(job.input_path)
		# Expected columns: CaseNumber, Article, Part, Point, Amount, RekvizitCode
		output_rows = []
		for _, row in df.iterrows():
			article = normalize_article(row.get("Article"))
			part = normalize_part(row.get("Part"))
			point = normalize_point(row.get("Point"))
			amount = normalize_amount(row.get("Amount"))
			rekvizit_code = row.get("RekvizitCode")
			rekvizit_name = map_rekvizit_code(rekvizit_code)

			check_status = "Error"
			error_type = None
			expected_rekvizit = None
			expected_min = None
			expected_max = None
			source_url = None
			confidence = None

			if amount is None or article is None:
				check_status = "Error"
				error_type = "data_error"
			else:
				rule = find_rule(db, article, part, point)
				if not rule:
					check_status = "Error"
					error_type = "article_not_found"
				else:
					# Fill expected
					expected_rekvizit = rule.rekvizit
					expected_min = rule.min_amount
					expected_max = rule.max_amount
					source_url = rule.source_url
					confidence = rule.confidence

					# Check amount range
					amount_ok = True
					if expected_min is not None and amount < expected_min:
						amount_ok = False
					if expected_max is not None and amount > expected_max:
						amount_ok = False

					# Check rekvizit match if provided
					rekvizit_ok = True
					if rekvizit_name and rule.rekvizit:
						rekvizit_ok = rekvizit_name == rule.rekvizit

					if confidence is not None and confidence < 0.6:
						check_status = "Error"
						error_type = "needs_human_review"
					elif amount_ok and rekvizit_ok:
						check_status = "OK"
					else:
						check_status = "Error"
						error_type = "sum_range_mismatch" if not amount_ok else "rekvizit_mismatch"

			output_rows.append({
				**row.to_dict(),
				"CheckStatus": check_status,
				"ErrorType": error_type or "",
				"ExpectedRekvizit": expected_rekvizit or "",
				"ExpectedMin": expected_min if expected_min is not None else "",
				"ExpectedMax": expected_max if expected_max is not None else "",
				"RuleSource": source_url or "",
				"Confidence": confidence if confidence is not None else "",
			})

		out_df = pd.DataFrame(output_rows)
		os.makedirs(settings.outputs_dir, exist_ok=True)
		out_path = os.path.join(settings.outputs_dir, os.path.basename(job.input_path).replace(".xlsx", "_report.xlsx"))
		out_df.to_excel(out_path, index=False)

		job.status = "completed"
		job.output_path = out_path
		db.commit()
	except Exception as e:
		job = db.get(ProcessingJob, job_id)
		if job:
			job.status = "failed"
			job.error = str(e)
			db.commit()
	finally:
		db.close()

