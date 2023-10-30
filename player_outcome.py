from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import relationship
from database import Base


class PlayerOutcome(Base):
    __tablename__ = "player_outcomes"

    id = Column(Integer, primary_key=True)

    player_num = Column(Integer, nullable=False)

    username = Column(String, nullable=False)
    win = Column(Boolean, nullable=False, default=False, server_default='f')

    game_id = Column(String, ForeignKey("db_games.id"), nullable=False)
    game = relationship("DbGame", backref="player_outcomes")

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    __table_args__ = (
        Index("player_outcomes_idx_game_id_username", game_id, username),
        Index("player_outcomes_idx_username_win_game_id", username, win, game_id),
    )        
    