from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import Rule


router = APIRouter(prefix="/admin/rules", tags=["admin"])


@router.post("/{rule_id}/approve")
def approve_rule(rule_id: int, db: Session = Depends(get_db)):
	rule = db.get(Rule, rule_id)
	if not rule:
		raise HTTPException(status_code=404, detail="Rule not found")
	rule.status = "approved"
	db.commit()
	return {"status": "ok"}


@router.post("/{rule_id}/reject")
def reject_rule(rule_id: int, db: Session = Depends(get_db)):
	rule = db.get(Rule, rule_id)
	if not rule:
		raise HTTPException(status_code=404, detail="Rule not found")
	rule.status = "rejected"
	db.commit()
	return {"status": "ok"}

