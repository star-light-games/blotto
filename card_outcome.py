from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import relationship
from database import Base


class CardOutcome(Base):
    __tablename__ = "card_outcomes"

    id = Column(Integer, primary_key=True)

    card = Column(String, nullable=False)
    win = Column(Boolean, nullable=False, default=False, server_default='f')

    game_id = Column(String, ForeignKey("db_games.id"), nullable=False)
    game = relationship("DbGame", backref="card_outcomes")

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    __table_args__ = (
        Index("card_outcomes_idx_game_id_card", game_id, card),
        Index("card_outcomes_idx_card_win_game_id", card, win, game_id), 
    )        
    