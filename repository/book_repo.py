from typing import Optional, List

from sqlalchemy.orm import Session

from models.book import Book
from schemas.book_schema import BookCreate, BookUpdate


class BookRepository:
    """
    Repository layer for book table DB operations only.
    No business logic should live here.
    """

    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> Book:
        book = Book(**book_data.model_dump())
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def get_all_books(db: Session) -> List[Book]:
        return db.query(Book).order_by(Book.id.desc()).all()

    @staticmethod
    def get_available_books(db: Session) -> List[Book]:
        return db.query(Book).filter(Book.quantity > 0).order_by(Book.id.desc()).all()

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
        return db.query(Book).filter(Book.id == book_id).first()

    @staticmethod
    def search_books(db: Session, keyword: str) -> List[Book]:
        keyword = f"%{keyword}%"
        return (
            db.query(Book)
            .filter(
                (Book.title.ilike(keyword)) |
                (Book.author.ilike(keyword)) |
                (Book.category.ilike(keyword))
            )
            .order_by(Book.id.desc())
            .all()
        )

    @staticmethod
    def update_book(db: Session, book: Book, update_data: BookUpdate) -> Book:
        data = update_data.model_dump(exclude_unset=True)

        for key, value in data.items():
            setattr(book, key, value)

        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def delete_book(db: Session, book: Book) -> None:
        db.delete(book)
        db.commit()

    @staticmethod
    def reduce_book_stock(db: Session, book: Book, quantity: int) -> Book:
        """
        Deduct stock after successful checkout.
        Assumes stock validation already happened in service layer.
        """
        book.quantity -= quantity
        db.flush()  # keep transaction open; commit will happen in service layer
        return book