from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship

from database import Base


class Book(Base):
    """
    Book inventory table
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=True)
    book_type = Column(String(50), nullable=True, default="hardcopy")  # hardcopy / softcopy
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with bills
    bills = relationship("Bill", back_populates="book", cascade="all, delete")