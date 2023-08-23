
from abilities_list import ABILITIES


class CardTemplate:
    def __init__(self, name: str, abilities: list[str], cost: int, attack: int, health: int, creature_types: list[str]):
        self.name = name
        self.abilities = [ABILITIES[ability_name] for ability_name in abilities]
        self.cost = cost
        self.attack = attack
        self.health = health
        self.creature_types = creature_types

    def to_json(self):
        return {
            "name": self.name,
            "abilities": [a.to_json() for a in self.abilities],
            "cost": self.cost,
            "attack": self.attack,
            "health": self.health,
            "creatureTypes": self.creature_types,
        }
    
    @staticmethod
    def from_json(json: dict):
        return CardTemplate(json["name"], [ability["name"] for ability in json["abilities"]], json["cost"], json["attack"], json["health"], json["creatureTypes"])
    