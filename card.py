from typing import TYPE_CHECKING
from character import Character

from utils import generate_unique_id
from card_template import CardTemplate


class Card:
    def __init__(self, template: 'CardTemplate'):
        self.template = template
        self.id = generate_unique_id()

    def to_character(self, lane, owner_number, owner_username):
        return Character(self.template, lane, owner_number, owner_username)

    def to_json(self):
        return {
            "id": self.id,
            "template": self.template.to_json()
        }
    
    @staticmethod
    def from_json(json):
        card = Card(CardTemplate.from_json(json['template']))
        card.id = json['id']
        return card

    @staticmethod
    def from_template(template: 'CardTemplate'):
        return Card(template)


    def __repr__(self):
        return f"Card {self.id}: {self.template.name}"
