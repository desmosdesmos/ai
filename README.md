UK RF Excel Checker (MVP)

Features
- Upload Excel with cases; async processing; download annotated report
- Rules DB with approve/reject; basic Admin UI
- Celery worker, Redis; Docker Compose
- Tests for normalization and rule lookup

Run locally (without Docker)
1) Install deps:
   - python3 -m pip install -r requirements.txt
2) Init DB and seed sample rules:
   - python3 scripts/seed_rules.py
3) Start API:
   - uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
4) Start worker (in another terminal):
   - celery -A backend.worker.celery_app worker --loglevel=INFO
5) Generate sample Excel:
   - python3 scripts/gen_sample_excel.py

Docker (recommended)
- Requires Docker/Compose. Then:
  - docker compose build
  - docker compose up

Endpoints
- POST /upload
- GET /status/{job}
- GET /download/{job}
- GET /rules, POST /rules
- POST /admin/rules/{id}/approve, /reject
- GET / -> upload UI; GET /admin -> admin UI

Excel columns (required)
- CaseNumber, Article, Part, Point, Amount, RekvizitCode

Output columns (added)
- CheckStatus, ErrorType, ExpectedRekvizit, ExpectedMin, ExpectedMax, RuleSource, Confidence

