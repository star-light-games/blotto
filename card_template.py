from ability import Ability
from abilities_list import ABILITIES

from typing import TYPE_CHECKING

from card import Card


class CardTemplate:
    def __init__(self, name: str, abilities: list[str], cost: int, attack: int, health: int, creature_types: list[str]):
        self.name = name
        self.abilities = [ABILITIES[ability_name] for ability_name in abilities]
        self.cost = cost
        self.attack = attack
        self.health = health
        self.creature_types = creature_types


    def to_card(self) -> Card:
        return Card(self)


    def to_json(self):
        return {
            "name": self.name,
            "abilities": [a.to_json() for a in self.abilities],
            "cost": self.cost,
            "attack": self.attack,
            "health": self.health,
            "creature_types": self.creature_types,
        }