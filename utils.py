import secrets
import random
import math

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_state import GameState


def generate_unique_id():
    return secrets.token_hex(10)


def plural(x):
    return 's' if x != 1 else ''


def element_to_color(element):
    return {
        'Earth': 'green',
        'Fire': 'red',
        'Water': 'blue',
        'Air': 'yellow',
    }[element]

def shuffled(l):
    l = l[:]
    random.shuffle(l)
    return l

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def get_game_redis_key(game_id):
    return f'game:{game_id}'

def get_game_with_hidden_information_redis_key(game_id):
    return f'game:{game_id}:hidden'

def get_game_lock_redis_key(game_id):
    return f'game:{game_id}:lock'

def get_staged_game_redis_key(game_id, player_num):
    return f'game:{game_id}:{player_num}:staged'

def get_staged_game_lock_redis_key(game_id, player_num):
    return f'game:{game_id}:{player_num}:staged:lock'

def get_staged_moves_redis_key(game_id, player_num):
    return f'game:{game_id}:{player_num}:staged:moves'

def get_deck_description_json_from_deck(deck):
    return {
        'name': deck['name'],
        'cards': [card['name'] for card in deck['card_templates']],
    }

def on_reveal_animation(lane_number: int, acting_player: int, from_character_index: int, game_state: 'GameState'):
    return {
        "event_type": "OnReveal",
        "data": {
            "lane": lane_number,
            "acting_player": acting_player,
            "from_character_index": from_character_index,
        },
        "game_state": game_state.to_json(),
    },    
