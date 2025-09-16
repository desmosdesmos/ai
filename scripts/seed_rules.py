import os
from backend.app.db import SessionLocal, engine
from backend.app.models.models import Rule, ProcessingJob, Base


def seed():
	Base.metadata.create_all(bind=engine)
	db = SessionLocal()
	try:
		count = db.query(Rule).count()
		if count == 0:
			items = [
				# 158 ч.3 п."в" — крупный размер 250k–1m (пример)
				Rule(
					article="158",
					part="3",
					point="в",
					rekvizit="крупный размер",
					min_amount=250000,
					max_amount=1000000,
					source_url="https://pravo.gov.ru/",
					confidence=0.92,
					status="approved",
				),
				# 159 ч.4 — особо крупный размер от 1m и выше (пример)
				Rule(
					article="159",
					part="4",
					point=None,
					rekvizit="особо крупный размер",
					min_amount=1000000,
					max_amount=None,
					source_url="https://pravo.gov.ru/",
					confidence=0.92,
					status="approved",
				),
				# 158 ч.2 — значительный ущерб 5k–250k (пример)
				Rule(
					article="158",
					part="2",
					point=None,
					rekvizit="значительный ущерб",
					min_amount=5000,
					max_amount=250000,
					source_url="https://pravo.gov.ru/",
					confidence=0.92,
					status="approved",
				),
			]
			for it in items:
				db.add(it)
			db.commit()
			print(f"Seeded {len(items)} rules")
		else:
			print("Rules already seeded, skipping")
	finally:
		db.close()


if __name__ == "__main__":
	seed()

