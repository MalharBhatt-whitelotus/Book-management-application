from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.book_schema import BookCreate, BookUpdate, BookRead
from services.book_services import BookService
from services.security import get_current_admin

router = APIRouter()


@router.get("/", response_model=List[BookRead])
async def get_books(
    db: AsyncSession = Depends(get_db),
    keyword: Optional[str] = Query(default=None)
):
    """
    Public / authenticated book listing.
    If keyword is passed, search by title/author/category.
    """
    if keyword:
        return await BookService.search_books(db, keyword)
    return await BookService.get_all_books(db)


@router.get("/available", response_model=List[BookRead])
async def get_available_books(db: AsyncSession = Depends(get_db)):
    """
    Books with stock > 0
    """
    return await BookService.get_available_books(db)


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await BookService.get_book_by_id(db, book_id)


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only: create book
    """
    return await BookService.create_book(db, book_data)


@router.put("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int,
    update_data: BookUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only: update book
    """
    return await BookService.update_book(db, book_id, update_data)


@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only: delete book
    """
    return await BookService.delete_book(db, book_id)