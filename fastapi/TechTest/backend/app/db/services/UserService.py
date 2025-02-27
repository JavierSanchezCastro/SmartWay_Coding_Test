from sqlalchemy.orm import Session
from db.daos.UserDAO import UserDAO
from pydantic import UUID4, EmailStr
from fastapi import status, HTTPException


class UserService:
    
    @staticmethod
    def get_by_uuid(uuid: UUID4, db: Session):
        user = UserDAO(db).get_by_uuid(uuid=uuid)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with uuid={uuid} not found")
        return user
    
    @staticmethod
    def get_by_email(email: EmailStr, db: Session):
        user = UserDAO(db).get_by_email(email=email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email={email} not found")
        return user

