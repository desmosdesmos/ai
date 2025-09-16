from typing import Optional
from pydantic import BaseModel


class JobCreateOut(BaseModel):
	job_id: str
	status: str


class JobStatusOut(BaseModel):
	job_id: str
	status: str
	output_url: Optional[str] = None
	error: Optional[str] = None

