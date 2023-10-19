import os

LOCAL = False
COMMON_DECK_USERNAME = 'COMMON_DECK'
BOT_DECK_USERNAME = 'BOT_DECK'
DATABASE_URL = "postgresql://bb:blotto@localhost:5432/bb"
EXTRA_TIME_ON_FIRST_TURN = 5

if os.path.exists('local_settings.py'):
    from local_settings import *