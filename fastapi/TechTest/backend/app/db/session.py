from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.Settings import settings

SQLALCHEMY_DATABASE_URL = settings.DB_URL.unicode_string()

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

#engine.echo = True

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

from contextlib import contextmanager
import traceback

#@contextmanager
def get_session() -> Generator: # pragma: no cover
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"Rolling Back [{e}]")
        #print(traceback.format_exc())
        db.rollback()
        raise
    finally:
        print("Closing Session")
        db.close()

