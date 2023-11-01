from IPython import embed
from bot import find_bot_move_rufus
from card import Card
from database import SessionLocal
from db_card import DbCard
from db_deck import DbDeck, delete_db_deck
from game_state_record import GameStateRecord
from draft_pick import DraftPick
from draft_choice import DraftChoice
from card_outcome import CardOutcome
from player_outcome import PlayerOutcome
from card_balance_change_record import CardBalanceChangeRecord

from game_state import GameState
from deck import Deck
from card_template import CardTemplate
from card_templates_list import CARD_TEMPLATES
from card import Card
from game import Game
from game_info import GameInfo
from character import Character
from lane import Lane
from lane_rewards import LANE_REWARDS
from ability import Ability
from abilities_list import ABILITIES

from sqlalchemy.orm import joinedload

from redis_utils import *
from utils import *

def delete_all_decks_containing_card(card_name: str) -> None:
    sess = SessionLocal()

    cards = (
        sess.query(DbCard)
        .options(joinedload(DbCard.deck))
        .filter(DbCard.name == card_name)
        .all()
    )

    deleted_deck_ids = set()

    for card in cards:
        if card.deck.id not in deleted_deck_ids:
            deleted_deck_ids.add(card.deck_id)
            delete_db_deck(sess, card.deck)


def main():
    sess = SessionLocal()

    # add objects that you want to use in the shell to this dictionary
    user_ns = {
        "sess": sess, 
        "DbCard": DbCard,
        "DbDeck": DbDeck,
        "GameStateRecord": GameStateRecord,
        "rget_json": rget_json,
        "rset_json": rset_json,
        "rlock": rlock,
        "rdel": rdel,
        "get_game_redis_key": get_game_redis_key,
        "get_game_lock_redis_key": get_game_lock_redis_key,
        "get_game_with_hidden_information_redis_key": get_game_with_hidden_information_redis_key,
        "get_staged_game_redis_key": get_staged_game_redis_key,
        "get_staged_game_lock_redis_key": get_staged_game_lock_redis_key,
        "get_staged_moves_redis_key": get_staged_moves_redis_key,
        "get_deck_description_json_from_deck": get_deck_description_json_from_deck,
        "run_with_timeout": run_with_timeout,
        "generate_unique_id": generate_unique_id,
        "CARD_TEMPLATES": CARD_TEMPLATES,
        "CardTemplate": CardTemplate,
        "Card": Card,
        "Deck": Deck,
        "GameState": GameState,
        "Game": Game,
        "GameInfo": GameInfo,
        "Character": Character,
        "Lane": Lane,
        "LANE_REWARDS": LANE_REWARDS,
        "Ability": Ability,
        "ABILITIES": ABILITIES,
        "find_bot_move_rufus": find_bot_move_rufus,
        "DraftPick": DraftPick,
        "DraftChoice": DraftChoice,
        "CardOutcome": CardOutcome,
        "PlayerOutcome": PlayerOutcome,
        "CardBalanceChangeRecord": CardBalanceChangeRecord,
    }

    embed(user_ns=user_ns)

    sess.close()

if __name__ == "__main__":
    main()

