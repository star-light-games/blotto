from sqlalchemy import Column, Index, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# We only actually store these object for cards in decks 
class DbCard(Base):
    __tablename__ = "db_cards"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    deck_id = Column(Integer, ForeignKey("db_decks.id"))
    deck = relationship("DbDeck", backref="cards")

    __table_args__ = (
        Index("db_cards_idx_deck_name", deck_id, name),
    )