import random
from card_template import CardTemplate
from utils import generate_unique_id
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lane import Lane


class Character:
    def __init__(self, template: CardTemplate, lane: 'Lane', owner_number: int, owner_username: str):
        self.id = generate_unique_id()
        self.template = template
        self.current_health = template.health
        self.max_health = template.health
        self.current_attack = template.attack
        self.shackled_turns = 0
        self.has_attacked = False
        self.owner_number = owner_number
        self.owner_username = owner_username
        self.lane = lane
        self.new = True

    def is_defender(self):
        return any([ability.name == 'Defender' for ability in self.template.abilities])
    
    def is_attacker(self):
        return any([ability.name == 'Attacker' for ability in self.template.abilities])
    
    def has_ability(self, ability_name):
        return any([ability_name == ability.name for ability in self.template.abilities])

    def attack(self, attacking_player: int, 
               damage_by_player: dict[int, int], 
               defending_characters: list['Character'], 
               lane_number: int,
               log: list[str]):
        self.has_attacked = True
        defenders = [character for character in defending_characters if character.is_defender()]
        if len(defenders) == 0 and not self.is_attacker:
            damage_by_player[attacking_player] += self.current_attack
            log.append(f"{self.owner_username}'s {self.template.name} dealt {self.template.attack} damage to the enemy player in Lane {lane_number}.")
        else:
            if len(defenders) == 0:
                target_character = random.choice(defending_characters)
            else:
                target_character = random.choice(defenders)
            self.fight(target_character, log)
            log.append(f"{self.owner_username}'s {self.template.name} dealt {self.template.attack} damage to the enemy {target_character.template.name} in Lane {lane_number}.")
                
                
    def punch(self, defending_character: 'Character', log: list[str]):
        if self.has_ability('Deathtouch'):
            defending_character.current_health = 0
            log.append(f"{self.owner_username}'s {self.template.name} deathtouched {defending_character.owner_username}'s {defending_character.template.name}.")
        else:
            defending_character.current_health -= self.current_attack

        if defending_character.has_ability('OnSurviveDamagePump'):
            defending_character.current_attack += 1
            defending_character.current_health += 1
            defending_character.max_health += 1
            log.append(f"{defending_character.owner_username}'s {defending_character.template.name} got +1/+1 for surviving damage.")

    def fight(self, defending_character: 'Character', log: list[str]):
        defending_character.punch(self, log)
        self.punch(defending_character, log)


    def roll_turn(self, log: list[str]):
        self.has_attacked = False
        self.new = False
        if self.has_ability('StartOfTurnFullHeal'):
            self.current_health = self.template.health
            log.append(f"{self.owner_username}'s {self.template.name} healed to full health.")


    def do_on_reveal(self, log: list[str]):
        if self.has_ability('OnRevealShackle'):
            random_enemy_character = self.lane.get_random_enemy_character(self.owner_number)
            if random_enemy_character is not None:
                random_enemy_character.shackled_turns += 1
                log.append(f"{self.owner_username}'s {self.template.name} shackled {random_enemy_character.owner_username}'s {random_enemy_character.template.name}.")


    def to_json(self):
        return {
            "id": self.id,
            "template": self.template.to_json(),
            "current_health": self.current_health,
            "shackled_turns": self.shackled_turns,
            # Can't put lane in here because of infinite recursion
        }
