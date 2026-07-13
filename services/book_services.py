from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from repository.book_repo import BookRepository
from schemas.book_schema import BookCreate, BookUpdate


class BookService:
    """
    Handles business logic related to books / inventory.
    """

    @staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate):
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

        return await BookRepository.create_book(db, book_data)

    @staticmethod
    async def get_all_books(db: AsyncSession):
        return await BookRepository.get_all_books(db)

    @staticmethod
    async def get_available_books(db: AsyncSession):
        return await BookRepository.get_available_books(db)

    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: int):
        book = await BookRepository.get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        return book

    @staticmethod
    async def search_books(db: AsyncSession, keyword: str):
        return await BookRepository.search_books(db, keyword)

    @staticmethod
    async def update_book(db: AsyncSession, book_id: int, update_data: BookUpdate):
        book = await BookRepository.get_book_by_id(db, book_id)
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

        return await BookRepository.update_book(db, book, update_data)

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int):
        book = await BookRepository.get_book_by_id(db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )

        await BookRepository.delete_book(db, book)
        return {"message": f"Book with id {book_id} deleted successfully"}
    
    @staticmethod
    async def filter_and_sort_books(
        db: AsyncSession,
        category: str | None = None,
        author: str | None = None,
        book_type: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        available: bool | None = None,
        sort_by: str = "id",
        order: str = "asc"
        ):
        return await BookRepository.filter_and_sort_books(
            db=db,
            category=category,
            author=author,
            book_type=book_type,
            min_price=min_price,
            max_price=max_price,
            available=available,
            sort_by=sort_by,
            order=order
            )