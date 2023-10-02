from typing import TYPE_CHECKING

from sqlalchemy import Column, Index, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

if TYPE_CHECKING:
    from db_card import DbCard

# We only actually store these object for cards in decks 
class DbDeck(Base):
    __tablename__ = "db_decks"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)

    cards: list['DbCard']

    __table_args__ = (
        Index("db_decks_idx_username_name", username, name),
    )