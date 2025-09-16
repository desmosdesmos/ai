import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from ..config import get_settings
from ..db import SessionLocal
from ..models.models import ProcessingJob


router = APIRouter(prefix="/status", tags=["jobs"])


@router.get("/{job_id}")
def get_status(job_id: str):
	db = SessionLocal()
	try:
		job = db.get(ProcessingJob, job_id)
		if not job:
			raise HTTPException(status_code=404, detail="Job not found")
		data = {"job_id": job.id, "status": job.status}
		if job.output_path:
			data["output_url"] = f"/download/{job.id}"
		if job.error:
			data["error"] = job.error
		return JSONResponse(data)
	finally:
		db.close()


download_router = APIRouter(prefix="/download", tags=["jobs"])


@download_router.get("/{job_id}")
def download(job_id: str):
	settings = get_settings()
	db = SessionLocal()
	try:
		job = db.get(ProcessingJob, job_id)
		if not job or not job.output_path:
			raise HTTPException(status_code=404, detail="Report not ready")
		filepath = job.output_path
		if not os.path.exists(filepath):
			raise HTTPException(status_code=404, detail="File not found")
		filename = os.path.basename(filepath)
		return FileResponse(filepath, filename=filename, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	finally:
		db.close()

