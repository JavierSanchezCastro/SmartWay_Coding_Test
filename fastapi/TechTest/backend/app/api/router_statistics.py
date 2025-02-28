from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/statistics")
async def show_statistics(request: Request):
    # Renderizar la plantilla con las imágenes
    return templates.TemplateResponse("statistics.html", {"request": request})