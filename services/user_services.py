from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config import settings
from repository.user_repo import UserRepository
from schemas.user_schema import UserRegister, UserLogin, Token
from services.security import (
    hash_password,
    authenticate_user,
    create_access_token
)


class UserService:
    """
    Handles user registration, login and user-related business logic.
    """

    @staticmethod
    def register_user(db: Session, user_data: UserRegister):
        # Check duplicate username
        existing_username = UserRepository.get_user_by_username(db, user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        # Check duplicate email
        existing_email = UserRepository.get_user_by_email(db, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        hashed_password = hash_password(user_data.password)

        user = UserRepository.create_user(
            db=db,
            name=user_data.name,
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            role="user"
        )
        return user

    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> Token:
        user = authenticate_user(db, login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        access_token = create_access_token(
            data={
                "sub": user.username,
                "role": user.role,
                "user_id": user.id
            },
            expires_delta=access_token_expires
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            role=user.role,
            username=user.username
        )

    @staticmethod
    def get_user_profile(user):
        return user

    @staticmethod
    def create_default_admin_if_not_exists(db: Session):
        """
        Auto-create default admin from .env if it does not exist.
        Call this during app startup in main.py later.
        """
        admin = UserRepository.get_user_by_username(db, settings.ADMIN_DEFAULT_USERNAME)
        if admin:
            return admin

        hashed_password = hash_password(settings.ADMIN_DEFAULT_PASSWORD)

        admin = UserRepository.create_user(
            db=db,
            name="System Admin",
            username=settings.ADMIN_DEFAULT_USERNAME,
            email=settings.ADMIN_DEFAULT_EMAIL,
            password_hash=hashed_password,
            role="admin"
        )
        return admin