import random
from card_template import CardTemplate
from utils import generate_unique_id
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from lane import Lane
    from game_state import GameState


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
               log: list[str],
               animations: list,
               game_state: 'GameState'):
        self.has_attacked = True
        maybe_also = ''
        defenders = [character for character in defending_characters if character.is_defender() and character.can_fight()]
        if len(defenders) == 0 and not self.is_attacker():
            multiplier = 2 if self.has_ability('DoubleTowerDamage') else 1
            damage_dealt = self.current_attack * multiplier
            damage_by_player[attacking_player] += damage_dealt
            if self.has_ability('OnTowerAttackDealMassDamage'):
                for character in defending_characters:
                    character.current_health -= 2
                    log.append(f"{self.owner_username}'s {self.template.name} dealt 2 damage to {character.owner_username}'s {character.template.name} in Lane {lane_number + 1}. "
                                f"{character.template.name}'s health is now {character.current_health}.")
            log.append(f"{self.owner_username}'s {self.template.name} dealt {damage_dealt} damage to the enemy player in Lane {lane_number + 1}.")
            
            animations.append([
                {
                    "event_type": "tower_damage",
                    "attacking_character_id": self.id,
                    "lane_number": lane_number,
                    "lane_damage_post_attack": damage_by_player[attacking_player],
                    "attacking_player": attacking_player,
                    "attacking_character_array_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                }, game_state.to_json()])
        else:
            if len(defenders) == 0:
                if len(defending_characters) > 0:
                    target_character = random.choice(defending_characters)
                else:
                    target_character = None
            else:
                target_character = random.choice(defenders)
            if target_character is not None:
                maybe_also = ' also'
                self.fight(target_character, lane_number, log, animations, game_state)
            if self.is_attacker():
                damage_by_player[attacking_player] += self.current_attack
                log.append(f"{self.owner_username}'s {self.template.name}{maybe_also} dealt {self.current_attack} damage to the enemy player in Lane {lane_number + 1}.")
                animations.append([{
                                "event_type": "tower_damage",
                                "attacking_character_id": self.id,
                                "lane_number": lane_number,
                                "lane_damage_post_attack": damage_by_player[attacking_player],
                                "attacking_player": attacking_player,
                                "attacking_character_array_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                            }, game_state.to_json()])
                
                
    def punch(self, defending_character: 'Character', lane_number: int, log: list[str], animations: list, game_state: 'GameState',
              starting_current_attack: Optional[int] = None):
        if self.has_ability('Deathtouch'):
            defending_character.current_health = 0
            log.append(f"{self.owner_username}'s {self.template.name} deathtouched {defending_character.owner_username}'s {defending_character.template.name}.")
        else:
            defending_character.current_health -= starting_current_attack if starting_current_attack is not None else self.current_attack
            log.append(f"{self.owner_username}'s {self.template.name} dealt {self.template.attack} damage to the enemy {defending_character.template.name} in Lane {lane_number + 1}. "
                        f"{defending_character.template.name}'s health is now {defending_character.current_health}.")

        if defending_character.has_ability('OnSurviveDamagePump') and defending_character.current_health > 0:
            defending_character.current_attack += 1
            defending_character.current_health += 1
            defending_character.max_health += 1
            log.append(f"{defending_character.owner_username}'s {defending_character.template.name} got +1/+1 for surviving damage.")
            animations.append([{
                            "event_type": "character_pump",
                            "defending_character_id": defending_character.id,
                            "defending_character_health_post_pump": defending_character.current_health,
                            "defending_character_attack_post_pump": defending_character.current_attack,
                            "lane_number": lane_number,
                            "attacking_player": self.owner_number,
                            "attacking_character_array_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                        }, game_state.to_json()])

    def fight(self, defending_character: 'Character', lane_number: int, log: list[str], animations: list, game_state: 'GameState'):
        defender_starting_current_attack = defending_character.current_attack
        self.punch(defending_character, lane_number, log, animations, game_state)
        if not self.has_ability('InvincibilityWhileAttacking'):
            defending_character.punch(self, lane_number, log, animations, game_state, starting_current_attack=defender_starting_current_attack)

        animations.append([{
                        "event_type": "character_attack",
                        "attacking_character_id": self.id,
                        "defending_character_id": defending_character.id,
                        "defending_character_health_post_attack": defending_character.current_health,
                        "lane_number": lane_number,
                        "attacking_player": self.owner_number,
                        "attacking_character_array_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                        "defending_character_array_index": [c.id for c in self.lane.characters_by_player[1 - self.owner_number]].index(defending_character.id),
                    }, game_state.to_json()])

    def can_fight(self):
        return self.current_health > 0


    def can_attack(self):
        return self.can_fight() and not self.has_attacked and self.shackled_turns == 0


    def roll_turn(self, log: list[str], animations: list, game_state: 'GameState'):
        self.has_attacked = False
        self.new = False
        if self.has_ability('StartOfTurnFullHeal'):
            self.current_health = self.template.health
            log.append(f"{self.owner_username}'s {self.template.name} healed to full health.")
            animations.append([{
                            "event_type": "character_heal",
                            "character_id": self.id,
                            "character_health_post_heal": self.current_health,
                            "player": self.owner_number,
                            "lane_number": self.lane.lane_number,
                        }, game_state.to_json()])
        
        if self.shackled_turns > 0:
            log.append(f"{self.owner_username}'s {self.template.name} is shackled for {self.shackled_turns} more turns.")
            animations.append([{
                            "event_type": "character_shackled",
                            "character_id": self.id,
                            "character_shackled_turns": self.shackled_turns,
                            "player": self.owner_number,
                            "lane_number": self.lane.lane_number,
                        }, game_state.to_json()])
            self.shackled_turns -= 1



    def do_on_reveal(self, log: list[str], animations: list, game_state: 'GameState'):
        if self.new:
            if self.has_ability('OnRevealShackle'):
                random_enemy_character = self.lane.get_random_enemy_character(self.owner_number)
                if random_enemy_character is not None:
                    random_enemy_character.shackled_turns += 1
                    log.append(f"{self.owner_username}'s {self.template.name} shackled {random_enemy_character.owner_username}'s {random_enemy_character.template.name}.")
                    animations.append([
                        {
                            "event_type": "character_shackle",
                            "shackling_character_id": self.id,
                            "shackled_character_id": random_enemy_character.id,
                            "character_shackled_turns": random_enemy_character.shackled_turns,
                            "player": self.owner_number,
                            "lane_number": self.lane.lane_number,
                            "shackling_character_array_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                            "shackled_character_array_index": [c.id for c in self.lane.characters_by_player[1 - self.owner_number]].index(random_enemy_character.id),
                        },
                        game_state.to_json(),
                    ])

            if self.has_ability('OnRevealPumpFriends'):
                for character in self.lane.characters_by_player[self.owner_number]:
                    character.current_attack += 1
                    character.current_health += 1
                    character.max_health += 1
                    log.append(f"{self.owner_username}'s {self.template.name} pumped {character.owner_username}'s {character.template.name}.")
                animations.append([
                    {
                        "event_type": "on_reveal",
                        "pumping_character_id": self.id,
                        "player": self.owner_number,
                        "lane_number": self.lane.lane_number,
                        "pumping_character_array_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                    },
                    game_state.to_json(),
                ])

            if self.has_ability('OnRevealPumpAttackers'):
                for character in self.lane.characters_by_player[self.owner_number]:
                    if character.is_attacker():
                        character.current_attack += 2
                        character.current_health += 2
                        character.max_health += 2
                        log.append(f"{self.owner_username}'s {self.template.name} pumped {character.owner_username}'s {character.template.name}.")
                animations.append([
                    {
                        "event_type": "on_reveal",
                        "pumping_character_id": self.id,
                        "player": self.owner_number,
                        "lane_number": self.lane.lane_number,
                        "pumping_character_array_index": [c.id for c in self.lane.characters_by_player[self.owner_number]].index(self.id),
                    },
                    game_state.to_json(),
                ])

            count_of_characters_with_pump_friendlies_ability = len([character for character in self.lane.characters_by_player[self.owner_number] if character.has_ability('PumpAttackOfCharactersPlayedHere')])
            self.current_attack += count_of_characters_with_pump_friendlies_ability




    def to_json(self):
        return {
            "id": self.id,
            "template": self.template.to_json(),
            "current_health": self.current_health,
            "shackled_turns": self.shackled_turns,
            "max_health": self.max_health,
            "current_attack": self.current_attack,
            "has_attacked": self.has_attacked,
            "owner_number": self.owner_number,
            "owner_username": self.owner_username,
            "new": self.new,            
            # Can't put lane in here because of infinite recursion
        }


    @staticmethod
    def from_json(json: dict, lane: 'Lane'):
        character = Character(
            template=CardTemplate.from_json(json['template']),
            lane=lane,
            owner_number=json['owner_number'],
            owner_username=json['owner_username'],
        )
        character.id = json['id']
        character.current_health = json['current_health']
        character.shackled_turns = json['shackled_turns']
        character.max_health = json['max_health']
        character.current_attack = json['current_attack']
        character.has_attacked = json['has_attacked']
        character.new = json['new']
        return character