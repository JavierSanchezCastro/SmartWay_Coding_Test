from sqlalchemy.orm import Session
from sqlalchemy import select
from db.daos.BaseDAO import BaseDAO
from db.models.Book import Book, Book_Status
from pydantic import UUID4

class BookDAO(BaseDAO):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def create(self, book: dict) -> Book:
        book = Book(**book)
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book
    
    def get_by_status(self, status: Book_Status) ->  list[Book]:
        return self.session.scalars(select(Book).where(Book.status == status)).all()
    
    def get_by_id(self, id: int) -> Book | None:
        self.session.get(Book, id)

    def get_by_uuid(self, uuid: UUID4) -> Book | None:
        return self.session.scalars(select(Book).where(Book.uuid == str(uuid))).first()

    def get_by_title(self, title: str) -> Book | None:
        return self.session.scalars(select(Book).where(Book.title == title)).first()

    def get_all(self) -> list[Book]:
        return self.session.scalars(select(Book)).all()

    def update(self):
        raise NotImplementedError