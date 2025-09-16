import os
from functools import lru_cache


class Settings:
	app_name: str = os.getenv("APP_NAME", "ukrf-checker")
	debug: bool = os.getenv("DEBUG", "false").lower() == "true"

	# Database
	database_url: str = os.getenv(
		"DATABASE_URL",
		# Default to SQLite for MVP
		"sqlite:////workspace/data/ukrf_checker.db",
	)

	# Celery / Redis
	redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
	broker_url: str = os.getenv("CELERY_BROKER_URL", redis_url)
	result_backend: str = os.getenv("CELERY_RESULT_BACKEND", redis_url)

	# File storage
	inputs_dir: str = os.getenv("INPUTS_DIR", "/workspace/data/inputs")
	outputs_dir: str = os.getenv("OUTPUTS_DIR", "/workspace/data/outputs")

	# Origins for CORS (if adding frontend)
	allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")


@lru_cache
def get_settings() -> Settings:
	return Settings()

