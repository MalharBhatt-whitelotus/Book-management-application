from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repository.book_repo import BookRepository
from schemas.book_schema import BookCreate, BookUpdate


class BookService:
    """
    Handles business logic related to books / inventory.
    """

    @staticmethod
    def create_book(db: Session, book_data: BookCreate):
        if book_data.quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity cannot be negative"
            )

        if book_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price must be greater than zero"
            )

        return BookRepository.create_book(db, book_data)

    @staticmethod
    def get_all_books(db: Session):
        return BookRepository.get_all_books(db)

    @staticmethod
    def get_available_books(db: Session):
        return BookRepository.get_available_books(db)

    @staticmethod
    def get_book_by_id(db: Session, book_id: int):
        book = BookRepository.get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        return book

    @staticmethod
    def search_books(db: Session, keyword: str):
        return BookRepository.search_books(db, keyword)

    @staticmethod
    def update_book(db: Session, book_id: int, update_data: BookUpdate):
        book = BookRepository.get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )

        if update_data.quantity is not None and update_data.quantity < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity cannot be negative"
            )

        if update_data.price is not None and update_data.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price must be greater than zero"
            )

        return BookRepository.update_book(db, book, update_data)

    @staticmethod
    def delete_book(db: Session, book_id: int):
        book = BookRepository.get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )

        BookRepository.delete_book(db, book)
        return {"message": f"Book with id {book_id} deleted successfully"}