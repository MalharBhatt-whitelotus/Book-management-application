from typing import List, Optional

from sqlalchemy.orm import Session

from models.bill import Bill


class BillsRepository:
    """
    Repository layer for bill table DB operations only.
    """

    @staticmethod
    def create_bill_rows(db: Session, bill_rows: List[Bill]) -> List[Bill]:
        """
        Adds multiple bill rows to the current transaction.
        Does not commit automatically because checkout should remain transactional.
        """
        db.add_all(bill_rows)
        db.flush()
        return bill_rows

    @staticmethod
    def get_bill_by_id(db: Session, bill_id: int) -> Optional[Bill]:
        return db.query(Bill).filter(Bill.id == bill_id).first()

    @staticmethod
    def get_bills_by_order_group(db: Session, order_group: str) -> List[Bill]:
        return (
            db.query(Bill)
            .filter(Bill.order_group == order_group)
            .order_by(Bill.id.asc())
            .all()
        )

    @staticmethod
    def get_all_bills(db: Session) -> List[Bill]:
        return db.query(Bill).order_by(Bill.id.desc()).all()

    @staticmethod
    def get_bills_by_user_id(db: Session, user_id: int) -> List[Bill]:
        return (
            db.query(Bill)
            .filter(Bill.user_id == user_id)
            .order_by(Bill.id.desc())
            .all()
        )