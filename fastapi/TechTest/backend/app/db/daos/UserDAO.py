from sqlalchemy.orm import Session
from sqlalchemy import select
from db.daos.BaseDAO import BaseDAO
from db.models.User import User
from pydantic import UUID4, EmailStr

class UserDAO(BaseDAO):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def create(self, user: dict) -> User:
        user = User(**user)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, id: int) -> User | None:
        self.session.get(User, id)

    def get_by_uuid(self, uuid: UUID4) -> User | None:
        return self.session.scalars(select(User).where(User.uuid == str(uuid))).first()
    
    def get_by_email(self, email: EmailStr) -> User | None:
        return self.session.scalars(select(User).where(User.email == email)).first()

    def get_all(self) -> list[User]:
        return self.session.scalars(select(User)).all()

    def update(self):
        raise NotImplementedError