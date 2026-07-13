from typing import Optional, List

from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    """
    Repository layer for user table DB operations only.
    """

    @staticmethod
    def create_user(
        db: Session,
        name: str,
        username: str,
        email: str,
        password_hash: str,
        role: str = "user"
    ) -> User:
        user = User(
            name=name,
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_all_users(db: Session) -> List[User]:
        return db.query(User).order_by(User.id.desc()).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username_or_email(db: Session, value: str) -> Optional[User]:
        return db.query(User).filter(
            (User.username == value) | (User.email == value)
        ).first()