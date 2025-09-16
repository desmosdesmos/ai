from celery import Celery
import os
from ..app.config import get_settings


settings = get_settings()

celery_app = Celery(
	"ukrf_checker",
	broker=settings.broker_url,
	backend=settings.result_backend,
)

celery_app.conf.task_routes = {
	"backend.worker.tasks.*": {"queue": "default"},
}

# Expose the celery instance with name expected by CLI
app = celery_app

