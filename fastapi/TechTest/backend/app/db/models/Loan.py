from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from db.models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from db.models.User import User

class Loan(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    loan_date: Mapped[datetime]
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="loans")
    book: Mapped["Book"] = relationship("Book")

    __table_args__ = (UniqueConstraint("user_id", "book_id"), )
