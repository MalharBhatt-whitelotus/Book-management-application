from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.book_schema import BookCreate, BookUpdate, BookRead
from services.book_services import BookService
from services.security import get_current_admin, get_current_user

router = APIRouter()


@router.get("/", response_model=List[BookRead])
def get_books(
    db: Session = Depends(get_db),
    keyword: Optional[str] = Query(default=None)
):
    """
    Public / authenticated book listing.
    If keyword is passed, search by title/author/category.
    """
    if keyword:
        return BookService.search_books(db, keyword)
    return BookService.get_all_books(db)


@router.get("/available", response_model=List[BookRead])
def get_available_books(db: Session = Depends(get_db)):
    """
    Books with stock > 0
    """
    return BookService.get_available_books(db)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return BookService.get_book_by_id(db, book_id)


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only: create book
    """
    return BookService.create_book(db, book_data)


@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    update_data: BookUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only: update book
    """
    return BookService.update_book(db, book_id, update_data)


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only: delete book
    """
    return BookService.delete_book(db, book_id)