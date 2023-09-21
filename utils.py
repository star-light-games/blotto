import secrets
import random
import math


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

def get_deck_description_json_from_deck(deck):
    return {
        'name': deck['name'],
        'cards': [card['name'] for card in deck['card_templates']],
    }
