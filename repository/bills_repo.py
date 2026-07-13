from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.bill import Bill


class BillsRepository:
    """
    Repository layer for bill table DB operations only.
    """

    @staticmethod
    async def create_bill_rows(db: AsyncSession, bill_rows: List[Bill]) -> List[Bill]:
        """
        Adds multiple bill rows to the current transaction.
        Does not commit automatically because checkout should remain transactional.
        """
        db.add_all(bill_rows)
        await db.flush()
        return bill_rows

    @staticmethod
    async def get_bill_by_id(db: AsyncSession, bill_id: int) -> Optional[Bill]:
        result = await db.execute(select(Bill).where(Bill.id == bill_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_bills_by_order_group(db: AsyncSession, order_group: str) -> List[Bill]:
        result = await db.execute(select(Bill)
            .where(Bill.order_group == order_group)
            .order_by(Bill.id.asc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_all_bills(db: AsyncSession) -> List[Bill]:
        result = await db.execute(select(Bill).order_by(Bill.id.desc()))
        return result.scalars().all()

    @staticmethod
    async def get_bills_by_user_id(db: AsyncSession, user_id: int) -> List[Bill]:
        result = await db.execute(select(Bill)
            .where(Bill.user_id == user_id)
            .order_by(Bill.id.desc())
        )
        return result.scalars().all()