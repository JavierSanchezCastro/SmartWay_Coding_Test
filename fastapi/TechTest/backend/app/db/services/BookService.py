from sqlalchemy.orm import Session
from db.daos.BookDAO import BookDAO
from pydantic import UUID4
from fastapi import status, HTTPException


class BookService:
    
    @staticmethod
    def get_by_uuid(uuid: UUID4, db: Session):
        book = BookDAO(db).get_by_uuid(uuid=uuid)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with uuid={uuid} not found")
        return book
    
    @staticmethod
    def get_by_title(title: str, db: Session):
        book = BookDAO(db).get_by_title(title=title)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with title={title} not found")
        return book