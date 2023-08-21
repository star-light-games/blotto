from typing import TYPE_CHECKING

from utils import generate_unique_id
if TYPE_CHECKING:
    from card_template import CardTemplate


class Card:
    def __init__(self, template: 'CardTemplate'):
        self.template = template
        self.id = generate_unique_id()

    def to_json(self):
        return {
            "id": self.id,
            "template": self.template.to_json()
        }
    