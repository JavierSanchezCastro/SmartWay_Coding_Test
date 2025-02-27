from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from pydantic import UUID4


class BaseDAO(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def get_by_id(self, id: int):
        pass

