from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..models.models import Rule
from ..schemas.rule import RuleCreate, RuleOut


router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("", response_model=list[RuleOut])
def list_rules(db: Session = Depends(get_db)):
	stmt = select(Rule).order_by(Rule.id.desc()).limit(200)
	return list(db.execute(stmt).scalars().all())


@router.post("", response_model=RuleOut)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)):
	rule = Rule(
		article=payload.article,
		part=payload.part,
		point=payload.point,
		rekvizit=payload.rekvizit,
		min_amount=payload.min_amount,
		max_amount=payload.max_amount,
		source_url=payload.source_url,
		source_excerpt=payload.source_excerpt,
		confidence=payload.confidence,
		status=payload.status or "pending",
	)
	db.add(rule)
	db.commit()
	db.refresh(rule)
	return rule

