import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..config import get_settings
from ..db import SessionLocal
from ..models.models import ProcessingJob


router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("")
async def upload_excel(file: UploadFile = File(...)):
	settings = get_settings()
	if not file.filename.lower().endswith((".xlsx", ".xls")):
		raise HTTPException(status_code=400, detail="Only Excel files are supported")

	job_id = uuid.uuid4().hex
	input_path = os.path.join(settings.inputs_dir, f"{job_id}_{file.filename}")
	os.makedirs(settings.inputs_dir, exist_ok=True)
	with open(input_path, "wb") as f:
		f.write(await file.read())

	# Create job record
	db = SessionLocal()
	try:
		job = ProcessingJob(id=job_id, status="queued", input_path=input_path)
		db.add(job)
		db.commit()
	finally:
		db.close()

	# Enqueue async processing via Celery
	try:
		from backend.worker.tasks import process_excel_job
		process_excel_job.delay(job_id)
	except Exception:
		# Worker might not be up yet in dev
		pass

	return JSONResponse({"job_id": job_id, "status": "queued"})

