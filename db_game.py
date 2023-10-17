

from sqlalchemy import Column, DateTime, Index, String, func
from database import Base


class DbGame(Base):
    __tablename__ = "db_games"

    id = Column(String, primary_key=True)

    player_0_username = Column(String)
    player_1_username = Column(String)

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    __table_args__ = (
        Index("db_games_idx_player_0_username_created_at", player_0_username, created_at),
        Index("db_games_idx_player_1_username_created_at", player_1_username, created_at),
    )

    def __repr__(self):
        return f"<DbGame: {self.id}>"
    
    def to_json(self):
        return {
            "id": self.id,
            "player_0_username": self.player_0_username,
            "player_1_username": self.player_1_username,
            "created_at": self.created_at.timestamp(),
        }
