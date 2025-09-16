from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
	app = request.app
	templates = app.state.templates
	return templates.TemplateResponse("index.html", {"request": request})


@router.get("/admin", response_class=HTMLResponse)
def admin(request: Request):
	app = request.app
	templates = app.state.templates
	return templates.TemplateResponse("admin.html", {"request": request})

