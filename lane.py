import random
from typing import Optional
from character import Character


class Lane:
    def __init__(self, lane_number: int):
        self.damage_by_player: dict[int, int] = {0: 0, 1: 0}
        self.characters_by_player: dict[int, list[Character]] = {0: [], 1: []}
        self.lane_number = lane_number


    def roll_turn(self, log: list[str]) -> None:
        done_attacking_by_player = {0: False, 1: False}
        self.resolve_combat(done_attacking_by_player, log)


    def resolve_combat(self, done_attacking_by_player: dict[int, bool], log: list[str], attacking_player: Optional[int] = None) -> None:
        if attacking_player is None:
            attacking_player = random.randint(0, 1)
        self.player_single_attack(attacking_player, done_attacking_by_player, log)
        if done_attacking_by_player[1 - attacking_player]:
            if done_attacking_by_player[attacking_player]:
                return
            else:
                self.resolve_combat(done_attacking_by_player, log, attacking_player)
        else:
            self.resolve_combat(done_attacking_by_player, log, 1 - attacking_player)


    def player_single_attack(self, attacking_player: int, done_attacking_by_player: dict[int, bool], log: list[str]):
        characters_that_can_attack = [character for character in self.characters_by_player[attacking_player] if not character.has_attacked]            
        if len(characters_that_can_attack) == 0:
            done_attacking_by_player[attacking_player] = True
        else:
            character = random.choice(characters_that_can_attack)
            defending_characters = self.characters_by_player[1 - attacking_player]
            character.attack(attacking_player, self.damage_by_player, defending_characters, self.lane_number, log)

        for player_num in self.characters_by_player:
            self.characters_by_player[player_num] = [character for character in self.characters_by_player[player_num] if character.current_health > 0]


    def to_json(self):
        return {
            "damage_by_player": self.damage_by_player,
            "characters_by_player": {player: [character.to_json() for character in self.characters_by_player[player]] for player in self.characters_by_player},
        }
