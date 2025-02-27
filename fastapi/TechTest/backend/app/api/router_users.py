from fastapi import APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from db.services.UserService import UserService
from api.utils import SessionDB
from pydantic import UUID4, EmailStr
from db.daos.UserDAO import UserDAO

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_all(request: Request, db: SessionDB):
    users = UserDAO(db).get_all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@router.get("/uuid/{uuid}")
async def get_by_uuid(request: Request, uuid: UUID4, db: SessionDB):
    try:
        user = UserService.get_by_uuid(uuid=uuid, db=db)
        return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return templates.TemplateResponse("error.html", {"request": request, "message": e.detail}, status_code=status.HTTP_404_NOT_FOUND)
        raise e

@router.get("/email/{email}")
async def get_by_email(request: Request, email: EmailStr, db: SessionDB):
    try:
        user = UserService.get_by_email(email=email, db=db)
        return templates.TemplateResponse("user_detail.html", {"request": request, "user": user})
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return templates.TemplateResponse("error.html", {"request": request, "message": e.detail}, status_code=status.HTTP_404_NOT_FOUND)
        raise e


@router.get("/uuid/{uuid}/loans")
async def get_loans_by_uuid(request: Request, uuid: UUID4, db: SessionDB):
    user = UserService.get_by_uuid(uuid=uuid, db=db)
    return templates.TemplateResponse("loan_history.html", {"request": request, "user": user})

@router.get("/email/{uuid}/loans")
async def get_loans_by_email(request: Request, email: EmailStr, db: SessionDB):
    user = UserService.get_by_email(email=email, db=db)
    return templates.TemplateResponse("loan_history.html", {"request": request, "user": user})

