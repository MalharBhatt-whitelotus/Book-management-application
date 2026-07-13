from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.bill_schema import CheckoutRequest, BillResponse
from services.bills_services import BillsService
from services.security import get_current_user, get_current_admin

router = APIRouter()


@router.post("/checkout", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
async def checkout_books(
    checkout_data: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    User checkout route:
    - validate stock
    - create bill
    - reduce inventory
    """
    return await BillsService.checkout_books(db, current_user, checkout_data)


@router.get("/my")
async def get_my_bills(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Current logged-in user's bills
    """
    return await BillsService.get_user_bills(db, current_user)


@router.get("/order/{order_group}", response_model=BillResponse)
async def get_order_summary(
    order_group: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get one order-group summary
    """
    return await BillsService.get_bill_order_summary(db, order_group)


@router.get("/")
async def get_all_bills(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only: get all bills/orders
    """
    return await BillsService.get_all_bills(db)