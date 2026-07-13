from typing import Optional, List

from sqlalchemy import select,or_
from sqlalchemy.ext.asyncio import AsyncSession

from models.book import Book
from schemas.book_schema import BookCreate, BookUpdate


class BookRepository:
    """
    Repository layer for book table DB operations only.
    No business logic should live here.
    """

    @staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
        book = Book(**book_data.model_dump())
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book

    @staticmethod
    async def get_all_books(db: AsyncSession) -> List[Book]:
        result = await db.execute(select(Book).order_by(Book.id.desc()))
        return result.scalars().all()

    @staticmethod
    async def get_available_books(db: AsyncSession) -> List[Book]:
        result = await db.execute(select(Book).where(Book.quantity > 0).order_by(Book.id.desc()))
        return result.scalars().all()

    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: int) -> Optional[Book]:
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def search_books(db: AsyncSession, keyword: str) -> List[Book]:
        keyword = f"%{keyword}%"
        result = await db.execute(
            select(Book)
            .where( 
                or_(
                    Book.title.ilike(keyword) ,
                    Book.author.ilike(keyword) ,
                    Book.category.ilike(keyword)
                    )
                    ).order_by(Book.id.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def update_book(db: AsyncSession, book: Book, update_data: BookUpdate) -> Book:
        data = update_data.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(book, key, value)

        await db.commit()
        await db.refresh(book)
        return book

    @staticmethod
    async def delete_book(db: AsyncSession, book: Book) -> None:
        await db.delete(book)
        await db.commit()

    @staticmethod
    async def reduce_book_stock(db: AsyncSession, book: Book, quantity: int) -> Book:
        """
        Deduct stock after successful checkout.
        Assumes stock validation already happened in service layer.
        """
        book.quantity -= quantity
        await db.flush()  # keep transaction open; commit will happen in service layer
        return book