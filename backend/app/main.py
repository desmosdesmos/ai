from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .config import get_settings
from .db import Base, engine
from .routes import upload, jobs, rules, admin, root
from .routes import extractor, fetcher
import os


def create_app() -> FastAPI:
	settings = get_settings()
	app = FastAPI(title=settings.app_name, debug=settings.debug)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	# Mount static and templates (simple UI)
	base_dir = os.path.dirname(os.path.dirname(__file__))  # /workspace/backend/app -> /workspace/backend
	static_dir = os.path.join(base_dir, "static")
	templates_dir = os.path.join(base_dir, "app", "templates")
	app.mount("/static", StaticFiles(directory=static_dir), name="static")
	templates = Jinja2Templates(directory=templates_dir)
	app.state.templates = templates

	# Include routes
	app.include_router(upload.router)
	app.include_router(jobs.router)
	app.include_router(jobs.download_router)
	app.include_router(rules.router)
	app.include_router(admin.router)
	app.include_router(root.router)
	app.include_router(extractor.router)
	app.include_router(fetcher.router)

	return app


app = create_app()


# Create tables if not exist (MVP)
Base.metadata.create_all(bind=engine)

