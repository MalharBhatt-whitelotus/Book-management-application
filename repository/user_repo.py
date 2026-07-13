from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


class UserRepository:
    """
    Repository layer for user table DB operations only.
    """

    @staticmethod
    async def create_user(
        db: AsyncSession,
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
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_all_users(db: AsyncSession) -> List[User]:
        result = await db.execute(select(User).order_by(User.id.desc()))
        return result.scalars().all()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username_or_email(db: AsyncSession, value: str) -> Optional[User]:
        result = await db.execute(select(User).where(
            (User.username == value) | (User.email == value)
        ))
        return result.scalar_one_or_none()