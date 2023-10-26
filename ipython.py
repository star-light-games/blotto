from IPython import embed
from card import Card
from database import SessionLocal
from db_card import DbCard
from db_deck import DbDeck
from game_state_record import GameStateRecord

from redis_utils import *
from utils import *

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
    }

    embed(user_ns=user_ns)

    sess.close()

if __name__ == "__main__":
    main()

