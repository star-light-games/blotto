from deck import Deck
from redis_utils import rget_json, rlock, rset_json
from settings import COMMON_DECK_USERNAME


COMMON_DECKS = [
    {
        'name': 'Learn to play',
        'cards': [
            'Ikki',
            'Pabu',
            'Meelo',
            'Roku',
            'Hakoda',
            'Prince Wu',
            'Visola',
            'Momo',
            'Tarrloq',
            'Southern Raider',
            'Naga',
            'Mai',
            'Opal',
            'Yon Rha',
            'Zaheer',
            'Fang',
            'Korra',
            'Master Pakku',
        ],
    },
    {
        'name': 'Healing Hands',
        'cards': [
            'Zuko',
            'Zuko',
            'Tonraq',
            'Mother Kya',
            'Mother Kya',
            'Kya',
            'Kya',
            'Katara',
            'Katara',
            'Sokka',
            'Sokka',
            'Hama',
            'Hama',
            'Ghazan',
            'Ghazan',
            'Unalaq',
            'Taqukaq',
            'Gran Gran Kanna',
            'Kyoshi',
        ]
    },
    {
        'name': 'Switcheroo',
        'cards': [
            'Monk Gyatso',
            'Monk Gyatso',
            'Ikki',
            'Momo',
            'Momo',
            'Yangchen',
            'Bumi II',
            'Opal',
            'Opal',
            'Appa',
            'Jinora',
            'Jinora',
            'Ming Hua',
            'Tenzin',
            'Tenzin',
            'Aang',
            'Aang',
            'Uncle Iroh',
        ]
    },
    {
        'name': 'Attack and Defense',
        'cards': [
            'Iroh II',
            'Iroh II',
            'Combustion Man',
            'Pabu',
            'Hiroshi',
            'Tonraq',
            'Izumi',
            'Izumi',
            'Tarrloq',
            'Tarrloq',
            'Riley',
            'Riley',
            'Sozin',
            'Sozin',
            'Mai',
            'Aang',
            'Fire Lord Ozai',
            'Master Pakku',
        ],
    },
    {
        'name': 'The Card Advantage',
        'cards': [
            'Hiroshi',
            'Hiroshi',
            'Tonraq',
            'Tonraq',
            'Dai Li Agent',
            'Kai',
            'Kai',
            'Prince Wu',
            'La',
            'La',
            'The Big Bad Hippo',
            'The Big Bad Hippo',
            'Appa',
            'Professor Zei',
            'Moon Spirit Yang',
            'Moon Spirit Yang',
            'The Boulder',
            'The Boulder',
        ]
    },
    {
        'name': 'Naked Aggression',
        'cards': [
            'Combustion Man',
            'Combustion Man',
            'Iroh II',
            'Iroh II',
            'Hakoda',
            'Hakoda',
            'Riley',
            'Opal',
            'Opal',
            'Sozin',
            'Sokka',
            'Ghazan',
            'Fang',
            'Fang',
            'Admiral Zhao',
            'Admiral Zhao',
            'Uncle Iroh',
            'Fire Lord Ozai',
        ]
    },
    {
        'name': 'Lock and Chain',
        'cards': [
            'Dai Li Agent',
            'Dai Li Agent',
            'Pabu',
            'Kuvira',
            'Kuvira',
            'Kai',
            'Kai',
            'La',
            'La',
            'Roku',
            'Baatar Jr',
            'Baatar Jr',
            'Mai',
            'Lin',
            'Lin',
            'Professor Zei',
            'Suyin',
            'Suyin',
        ]
    },
]


def create_common_decks():
    with rlock('decks'):
        decks_json = rget_json('decks') or {}

        for deck in COMMON_DECKS:
            if deck['name'] not in [d['name'] for d in decks_json.values()]:
                deck = Deck(deck['cards'], COMMON_DECK_USERNAME, deck['name'])
                deck_id = deck.id
                decks_json[deck_id] = deck.to_json()

        rset_json('decks', decks_json)
