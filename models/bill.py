from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import relationship

from database import Base


class Bill(Base):
    """
    Bill table

    This design stores one purchased book per bill row.
    If a user checks out multiple books in one checkout, the service layer
    can create multiple bill rows sharing the same order_group / order number.
    This keeps the architecture simple and beginner-friendly while still
    supporting multi-book checkout.
    """
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Order grouping id for one checkout containing multiple books
    order_group = Column(String(100), nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    customer_name = Column(String(150), nullable=False)
    book_title = Column(String(255), nullable=False)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)

    purchased_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bills")
    book = relationship("Book", back_populates="bills")