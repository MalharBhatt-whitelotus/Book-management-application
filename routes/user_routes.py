from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.user_schema import UserRegister, UserLogin, UserRead, Token
from services.user_services import UserService
from services.security import get_current_user
from models.user import User

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """
    Register a normal user
    """
    return await UserService.register_user(db, user_data)


@router.post("/login", response_model=Token)
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Login user/admin and return JWT token
    """
    return await UserService.login_user(db, login_data)


@router.get("/me", response_model=UserRead)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Return current logged-in user profile
    """
    return await UserService.get_user_profile(current_user)