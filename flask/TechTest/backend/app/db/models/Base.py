import uuid
from sqlalchemy.orm import as_declarative, DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime, timezone
from sqlalchemy.sql import func
from sqlalchemy import String, text
from flask_sqlalchemy.model import Model
from app.db.session import db


class Base(db.Model):
    __abstract__ = True  #Avoid creating this table
    __name__: str
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(
        String(36),
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
