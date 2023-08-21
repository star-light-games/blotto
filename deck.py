from card_templates_list import CARD_TEMPLATES


class Deck:
    def __init__(self, cards: list[str]):
        self.card_templates = [CARD_TEMPLATES[card_name] for card_name in cards]
        
    def to_draw_pile(self):
        return [card_template.to_card() for card_template in self.card_templates]