from fastapi import APIRouter
import requests


router = APIRouter(prefix="/fetch", tags=["fetcher"])


@router.get("/url")
def fetch_url(url: str):
	resp = requests.get(url, timeout=20)
	resp.raise_for_status()
	# For MVP, return plain text (sites may have HTML)
	return {"status": resp.status_code, "content": resp.text[:50000]}

