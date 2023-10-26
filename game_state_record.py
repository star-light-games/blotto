

from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import JSONB
from db_game import DbGame


class GameStateRecord(Base):
    __tablename__ = "game_state_records"

    id = Column(Integer, primary_key=True)

    game_id = Column(String, ForeignKey("db_games.id"))
    game = relationship(DbGame, backref="game_state_records")

    turn = Column(Integer, nullable=False)
    
    player_0_username = Column(String)
    player_1_username = Column(String)

    game_state = Column(JSONB)

    __table_args__ = (
        Index("game_state_records_idx_game_id_turn_number", game_id, turn),
        Index("game_state_records_idx_player_0_username_game_id_turn_number", player_0_username, game_id, turn),
        Index("game_state_records_idx_player_1_username_game_id_turn_number", player_1_username, game_id, turn),
    )

    def __repr__(self):
        return f"<GameStateRecord {self.id}: Game {self.game_id}, between {self.player_0_username} and {self.player_1_username}, turn {self.turn}>"