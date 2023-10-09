from typing import Optional

from sqlalchemy import Column, Index, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from utils import generate_unique_id

from db_card import DbCard

# We only actually store these object for cards in decks 
class DbDeck(Base):
    __tablename__ = "db_decks"

    id = Column(String, primary_key=True)
    username = Column(String)
    name = Column(String)
    associated_lane_reward_name = Column(String)

    # cards: list['DbCard']

    __table_args__ = (
        Index("db_decks_idx_username_name", username, name),
    )


def add_db_deck(sess, cards: list[str], username: str, deck_name: str, associated_lane_reward_name: Optional[str]) -> DbDeck:
    db_deck = DbDeck(
        id=generate_unique_id(),
        username=username,
        name=deck_name,
        associated_lane_reward_name=associated_lane_reward_name,
    )

    sess.add(db_deck)
    sess.commit()

    for card_name in cards:
        sess.add(DbCard(
            name=card_name,
            deck=db_deck,
        ))
    sess.commit()

    return db_deck