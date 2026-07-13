import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.bill import Bill
from models.user import User
from repository.book_repo import BookRepository
from repository.bills_repo import BillsRepository
from schemas.bill_schema import CheckoutRequest, BillResponse, BillItemResponse


class BillsService:
    """
    Handles checkout flow, bill generation and inventory deduction.
    """

    @staticmethod
    async def checkout_books(db: AsyncSession, current_user: User, checkout_data: CheckoutRequest) -> BillResponse:
        """
        Flow:
        1. Validate all books exist
        2. Validate requested stock
        3. Create bill rows
        4. Reduce stock
        5. Commit transaction
        6. Return bill summary
        """

        if not checkout_data.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No books selected for checkout"
            )

        order_group = f"ORD-{uuid.uuid4().hex[:10].upper()}"
        bill_rows: List[Bill] = []
        total_amount = 0.0

        try:
            for item in checkout_data.items:
                book = await BookRepository.get_book_by_id(db, item.book_id)

                if not book:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Book with id {item.book_id} not found"
                    )

                if item.quantity <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Quantity for book '{book.title}' must be greater than zero"
                    )

                if book.quantity < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=(
                            f"Insufficient stock for '{book.title}'. "
                            f"Available: {book.quantity}, requested: {item.quantity}"
                        )
                    )

                line_total = book.price * item.quantity
                total_amount += line_total

                bill_row = Bill(
                    order_group=order_group,
                    user_id=current_user.id,
                    book_id=book.id,
                    customer_name=current_user.name,
                    book_title=book.title,
                    quantity=item.quantity,
                    unit_price=book.price,
                    line_total=line_total
                )
                bill_rows.append(bill_row)

                # reduce stock in the same transaction
                await BookRepository.reduce_book_stock(db, book, item.quantity)

            # create all bill rows
            await BillsRepository.create_bill_rows(db, bill_rows)

            # commit full transaction only after all rows and stock changes succeed
            await db.commit()

            # refresh rows after commit
            for row in bill_rows:
                await db.refresh(row)

            return BillsService._build_bill_response(
                bill_rows=bill_rows,
                total_amount=total_amount,
                customer_name=current_user.name,
                order_group=order_group
            )

        except HTTPException:
            await db.rollback()
            raise
        except Exception as exc:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Checkout failed: {str(exc)}"
            )

    @staticmethod
    async def get_bill_by_id(db: AsyncSession, bill_id: int):
        bill = await BillsRepository.get_bill_by_id(db, bill_id)
        if not bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill with id {bill_id} not found"
            )
        return bill

    @staticmethod
    async def get_all_bills(db: AsyncSession):
        return  await BillsRepository.get_all_bills(db)

    @staticmethod
    async def get_user_bills(db: AsyncSession, current_user: User):
        return await BillsRepository.get_bills_by_user_id(db, current_user.id)

    @staticmethod
    async def get_bill_order_summary(db: AsyncSession, order_group: str) -> BillResponse:
        rows = await BillsRepository.get_bills_by_order_group(db, order_group)

        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No bill found for order group {order_group}"
            )

        total_amount = sum(row.line_total for row in rows)
        customer_name = rows[0].customer_name

        return BillsService._build_bill_response(
            bill_rows=rows,
            total_amount=total_amount,
            customer_name=customer_name,
            order_group=order_group
        )

    @staticmethod
    def _build_bill_response(
        bill_rows: List[Bill],
        total_amount: float,
        customer_name: str,
        order_group: str
    ) -> BillResponse:
        items = [
            BillItemResponse(
                bill_id=row.id,
                order_group=row.order_group,
                book_id=row.book_id,
                book_title=row.book_title,
                quantity=row.quantity,
                unit_price=row.unit_price,
                line_total=row.line_total,
                purchased_at=row.purchased_at
            )
            for row in bill_rows
        ]

        purchased_at = bill_rows[0].purchased_at if bill_rows else None

        return BillResponse(
            order_group=order_group,
            customer_name=customer_name,
            total_amount=round(total_amount, 2),
            items=items,
            purchased_at=purchased_at
        )