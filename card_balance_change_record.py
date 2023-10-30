

from sqlalchemy import Column, DateTime, Index, Integer, String, func
from database import Base


class CardBalanceChangeRecord(Base):
    __tablename__ = "card_balance_change_records"

    id = Column(Integer, primary_key=True)

    card = Column(String, nullable=False)

    card_template_str = Column(String, nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    __table_args__ = (
        Index("card_balance_change_records_idx_card_created_at", card, created_at),
    )