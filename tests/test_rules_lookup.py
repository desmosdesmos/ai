from backend.app.db import SessionLocal, engine
from backend.app.models.models import Base, Rule
from backend.app.services.rules_service import find_rule


def setup_module(module):
	Base.metadata.create_all(bind=engine)
	db = SessionLocal()
	try:
		db.query(Rule).delete()
		db.add(Rule(article="158", part="3", point="в", rekvizit="крупный размер", min_amount=250000, max_amount=1000000, status="approved"))
		db.add(Rule(article="158", part="2", point=None, rekvizit="значительный ущерб", min_amount=5000, max_amount=250000, status="approved"))
		db.commit()
	finally:
		db.close()


def test_find_rule_exact():
	db = SessionLocal()
	try:
		r = find_rule(db, "158", "3", "в")
		assert r is not None and r.rekvizit == "крупный размер"
	finally:
		db.close()


def test_find_rule_fallback_part():
	db = SessionLocal()
	try:
		r = find_rule(db, "158", "2", None)
		assert r is not None and r.rekvizit == "значительный ущерб"
	finally:
		db.close()

