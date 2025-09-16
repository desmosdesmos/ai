from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.models import Rule


def find_rule(db: Session, article: str, part: Optional[str], point: Optional[str]) -> Optional[Rule]:
	# 1) exact match
	stmt = (
		select(Rule)
		.where(Rule.article == article)
		.where((Rule.part == part) | (Rule.part.is_(None)))
		.where((Rule.point == point) | (Rule.point.is_(None)))
		.where(Rule.status == "approved")
	)
	results = db.execute(stmt).scalars().all()
	# Prefer most specific: article+part+point > article+part > article
	best = None
	best_score = -1
	for r in results:
		score = 0
		if r.part is not None and part is not None and r.part == part:
			score += 1
		if r.point is not None and point is not None and r.point == point:
			score += 1
		if score > best_score:
			best = r
			best_score = score
	return best

