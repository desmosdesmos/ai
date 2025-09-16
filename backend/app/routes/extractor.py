from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..services.extractor_service import extract_rules_from_text
from ..models.models import Rule


router = APIRouter(prefix="/extract", tags=["extractor"])


@router.post("/text")
def extract_from_text(article: str, text: str, db: Session = Depends(get_db)):
	items = extract_rules_from_text(text, article)
	created = []
	for it in items:
		rule = Rule(
			article=it.get("article") or article,
			part=it.get("part"),
			point=it.get("point"),
			rekvizit=it.get("rekvizit"),
			min_amount=it.get("min"),
			max_amount=it.get("max"),
			source_url=it.get("source_url"),
			source_excerpt=it.get("source_excerpt"),
			confidence=it.get("confidence", 0.5),
			status="pending",
		)
		db.add(rule)
		created.append(rule)
	db.commit()
	return {"created": [r.id for r in created]}

