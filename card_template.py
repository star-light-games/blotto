from typing import Callable, Union
from abilities_list import ABILITIES


class CardTemplate:
    def __init__(self, name: str, abilities: list[Union[str, tuple[str, int]]], cost: int, attack: int, health: int, creature_types: list[str], not_in_card_pool: bool = False):
        self.name = name
        self.abilities = []
        for ability in abilities:
            if isinstance(ability, tuple):
                self.abilities.append(ABILITIES[ability[0]](ability[1]))  # type: ignore
            else:
                self.abilities.append(ABILITIES[ability])

        self.cost = cost
        self.attack = attack
        self.health = health
        self.creature_types = creature_types
        self.not_in_card_pool = not_in_card_pool

    def to_json(self):
        return {
            "name": self.name,
            "abilities": [a.to_json() for a in self.abilities],
            "cost": self.cost,
            "attack": self.attack,
            "health": self.health,
            "creatureTypes": self.creature_types,
            **({"notInCardPool": self.not_in_card_pool} if self.not_in_card_pool else {}),
        }
    
    @staticmethod
    def from_json(json: dict):
        return CardTemplate(json["name"], [(ability["name"], ability["number"]) if ability.get("number") is not None else ability["name"] for ability in json["abilities"]], 
                            json["cost"], json["attack"], json["health"], json["creatureTypes"],
                            json["notInCardPool"] if "notInCardPool" in json else False)
    