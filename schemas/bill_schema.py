from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict


class CheckoutItem(BaseModel):
    book_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CheckoutRequest(BaseModel):
    items: List[CheckoutItem] = Field(..., min_length=1)


class BillItemResponse(BaseModel):
    bill_id: int
    order_group: str
    book_id: int
    book_title: str
    quantity: int
    unit_price: float
    line_total: float
    purchased_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BillResponse(BaseModel):
    order_group: str
    customer_name: str
    total_amount: float
    items: List[BillItemResponse]
    purchased_at: datetime