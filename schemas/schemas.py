"""Table Schemas"""
from enum import Enum
from typing import List
from datetime import datetime
from fastapi import UploadFile, File
from pydantic import BaseModel, ConfigDict, Field, field_validator

class BookRequest(BaseModel):
    """
    desc -> Validating book inputs
    args -> BaseModel
    returns -> None
    """
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., ge=150)
    quantity: int = Field(..., ge=1)
    book_type: str = Field(..., min_length=1, max_length=100)
    cover_file: UploadFile | None = File(None)
    document_file: UploadFile | None = File(None)

class BookResponse(BaseModel):
    """
    desc -> Validating book Ouputs
    args -> BaseModel
    returns -> None
    """
    id: int
    author : str
    price: float
    quantity: int
    book_type: str
    cover_file: File
    document_file: File

class UserRequest(BaseModel):
    """
    desc -> Validating user inputs.
    args -> Base Model
    returns -> None
    """
    username: str = Field(...)
    hashed_password: str = Field(...)

class UserResponse(BaseModel):
    """
    desc -> Validating user outputs.
    args -> BaseModel
    returns -> None
    """
    id: int
    username: str
    hashed_password: str

class BillRequest(BaseModel):
    """
    desc -> Validating bill inputs.
    args -> BaseModel
    return -> None
    """
    customer: str = Field(..., min_length=1, max_length=100)
    book: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., ge=1)
    created_at: datetime = Field(...)
    total_cost: float = Field(...)

class BillResponse(BaseModel):
    """
    desc -> Validating bill outputs.
    args -> BaseModel
    returns ->
    """
    id: int
    customer: str
    book: str
    quantity: int
    created_at: datetime
    total_cost: float