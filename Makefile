PY?=python3

.PHONY: venv install run api worker seed test sample

venv:
	$(PY) -m venv .venv
	. .venv/bin/activate && pip install -U pip
	. .venv/bin/activate && pip install -r requirements.txt

install:
	python3 -m pip install -r requirements.txt

run:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

worker:
	celery -A backend.worker.celery_app worker --loglevel=INFO

seed:
	python3 scripts/seed_rules.py

sample:
	python3 scripts/gen_sample_excel.py

test:
	pytest -q

