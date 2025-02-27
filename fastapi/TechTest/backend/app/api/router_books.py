from fastapi import APIRouter
from api.utils import SessionDB
from db.daos.BookDAO import BookDAO
from pydantic import UUID4
from db.services.BookService import BookService
from db.models.Book import Book_Status
from fastapi.requests import Request

router = APIRouter()
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_all(request: Request, db: SessionDB):
    books = BookDAO(db).get_all()
    return templates.TemplateResponse("books.html", {"request": request, "books": books, "page_title": "All Books", "header_text": "All Available and Borrowed Books"})

@router.get("/status/{status}")
async def get_by_status(request: Request, status: Book_Status, db: SessionDB):
    books = BookDAO(db).get_by_status(status=status)
    return templates.TemplateResponse("books.html", {"request": request, "books": books, "page_title": "Available Books", "header_text": f"{status.value} Books"})

@router.get("/uuid/{uuid}")
async def get_by_uuid(request: Request, uuid: UUID4, db: SessionDB):
    book = BookService.get_by_uuid(uuid=uuid, db=db)
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})

@router.get("/title/{title}")
async def get_by_title(title: str, db: SessionDB):
    return BookService.get_by_title(title=title, db=db)
