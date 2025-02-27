from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.models.Base import Base
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Numeric


class Book_Status(str, Enum):
    Borrowed = "Borrowed"
    Available = "Available"

class Book(Base):
    __table_args__ = {'extend_existing': True}
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    publish_date: Mapped[datetime]
    status: Mapped[Book_Status] = mapped_column(SQLAlchemyEnum(Book_Status), nullable=False, default=Book_Status.Available)
    pages: Mapped[int] = mapped_column(nullable=False, default=0)
    goodread_rating: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
