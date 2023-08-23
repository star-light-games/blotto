from card_templates_list import CARD_TEMPLATES
from utils import generate_unique_id

from card import Card
from card_template import CardTemplate

class Deck:
    def __init__(self, cards: list[str], username: str, name: str):
        self.id = generate_unique_id()
        self.card_templates = [CARD_TEMPLATES[card_name] for card_name in cards]
        self.username = username
        self.name = name
        
    def to_draw_pile(self):
        return [Card.from_template(card_template) for card_template in self.card_templates]
    
    def to_json(self):
        return {
            "id": self.id,
            "card_templates": [card_template.to_json() for card_template in self.card_templates],
            "username": self.username,
            "name": self.name,
        }
    
    @staticmethod
    def from_json(json):
        deck = Deck([CardTemplate.from_json(card_template).name for card_template in json['card_templates']], json['username'], json['name'])
        deck.id = json['id']
        return deck