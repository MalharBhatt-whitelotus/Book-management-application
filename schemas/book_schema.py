from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    description: Optional[str] = None
    book_type: Optional[str] = "hardcopy"


class BookCreate(BookBase):
    """
    Schema for admin creating a new book
    """
    pass


class BookUpdate(BaseModel):
    """
    Partial update schema for admin
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    book_type: Optional[str] = None


class BookRead(BookBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)