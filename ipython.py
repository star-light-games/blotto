from IPython import embed
from card import Card
from database import SessionLocal
from db_card import DbCard
from db_deck import DbDeck

from redis_utils import *
from utils import *

def main():
    sess = SessionLocal()

    # add objects that you want to use in the shell to this dictionary
    user_ns = {
        "sess": sess, 
        "DbCard": DbCard,
        "DbDeck": DbDeck,
    }

    embed(user_ns=user_ns)

    sess.close()

if __name__ == "__main__":
    main()

