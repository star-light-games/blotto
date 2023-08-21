import random
from card_template import CardTemplate
from utils import generate_unique_id


class Character:
    def __init__(self, template: CardTemplate):
        self.id = generate_unique_id()
        self.template = template
        self.current_health = template.health
        self.shackled_turns = 0
        self.has_attacked = False

    def is_defender(self):
        return any([ability.name == 'Defender' for ability in self.template.abilities])
    
    def is_attacker(self):
        return any([ability.name == 'Attacker' for ability in self.template.abilities])
    
    def attack(self, attacking_player: int, 
               damage_by_player: dict[int, int], 
               defending_characters: list['Character'], 
               lane_number: int,
               log: list[str]):
        self.has_attacked = True
        defenders = [character for character in defending_characters if character.is_defender()]
        if len(defenders) == 0 and not self.is_attacker:
            damage_by_player[attacking_player] += self.template.attack
            log.append(f"Player {attacking_player}'s dealt {self.template.attack} damage to the enemy player in Lane {lane_number}.")
        else:
            if len(defenders) == 0:
                target_character = random.choice(defending_characters)
                self.fight()

    def fight(self, defending_character: 'Character'):
        self.current_health -= defending_character.template.attack
        defending_character.current_health -= self.template.attack


    def to_json(self):
        return {
            "id": self.id,
            "template": self.template.to_json(),
            "current_health": self.current_health,
            "shackled_turns": self.shackled_turns,
        }
