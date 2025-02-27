from pydantic import UUID4
from app.db.models.Book import Book, Book_Status
from app.db.session import db
from app.books import bp
from flask import render_template
from sqlalchemy import select

@bp.route("/")
async def get_all():
    print("bokkkks", flush=True)
    books = Book.query.all()
    return render_template("books/books.html", books=books, page_title="All Books", header_text="All Available and Borrowed Books")
#    return templates.TemplateResponse("books.html", {"request": request, "books": books, "page_title": "All Books", "header_text": "All Available and Borrowed Books"})
#
@bp.route("/status/<status>")
async def get_by_status(status: Book_Status):
    print("hello")
    books = Book.query.filter_by(status=status).all()
    return render_template("books/books.html", books=books, page_title=f"{status} Books", header_text=f"{status} Books")
    #return templates.TemplateResponse("books.html", {"request": request, "books": books, "page_title": "Available Books", "header_text": f"{status.value} Books"})
#
@bp.route("/uuid/<uuid:uuid>")
async def get_by_uuid(uuid):
    book = Book.query.filter_by(uuid=str(uuid)).first_or_404()
    print(book)
    return render_template("books/book_detail.html", book=book)
