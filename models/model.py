"""Table creation"""
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime

from database import Base

class BookType(str, Enum):
    """
    desc -> check the book type
    args -> string, enum
    return -> Boolean 
    """
    hardcopy: str = "hardcopy"
    softcopy: str = "softcopy"

class Book(Base):
    """
    desc -> Book table creation
    args -> Base
    return -> None
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, unique=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=True)
    cover_file = Column(String, nullable=True)
    document_file = Column(String, nullage=False)
    book_type : BookType

class User(Base):
    """
    desc -> User table creation
    args -> Base
    return -> None
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False, unique=False)

class Bill(Base):
    """
    desc -> Bill table creation
    foreign_key -> Customer: User, Product: Book
    args -> Base
    return -> None
    """
    __tablename__ = "biils"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer = Column(String, ForeignKey("users.id"), nullable=False)
    book = Column(String, ForeignKey("books.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    total_cost = Column(Float, nullable=False)

    customer = relationship("User", back_populates="bills")
    book = relationship("Book", back_populates="bills")