from typing import TYPE_CHECKING
import random
from typing import Optional
from character import Character
if TYPE_CHECKING:
    from game_state import GameState


class Lane:
    def __init__(self, lane_number: int):
        self.damage_by_player: dict[int, int] = {0: 0, 1: 0}
        self.characters_by_player: dict[int, list[Character]] = {0: [], 1: []}
        self.lane_number = lane_number
        self.additional_combat_priority = 0


    def do_start_of_turn(self, log: list[str], animations: list, game_state: 'GameState') -> None:
        for player_num in [0, 1]:
            for character in self.characters_by_player[player_num]:
                character.escaped_death = False
                character.do_on_reveal(log, animations, game_state)        


    def roll_turn(self, log: list[str], animations: list, game_state: 'GameState') -> None:
        done_attacking_by_player = {0: False, 1: False}

        self.resolve_combat(done_attacking_by_player, log, animations, game_state)

        for player_num in done_attacking_by_player:
            for character in self.characters_by_player[player_num]:
                character.roll_turn(log, animations, game_state)

        self.additional_combat_priority = 0


    def resolve_combat(self, 
                       done_attacking_by_player: dict[int, bool], 
                       log: list[str], 
                       animations: list,
                       game_state: 'GameState',
                       attacking_player: Optional[int] = None) -> None:
        if attacking_player is None:
            attacking_player = random.randint(0, 1)
        self.player_single_attack(attacking_player, done_attacking_by_player, log, animations, game_state)
        if done_attacking_by_player[1 - attacking_player]:
            if done_attacking_by_player[attacking_player]:
                return
            else:
                self.resolve_combat(done_attacking_by_player, log, animations, game_state, attacking_player)
        else:
            self.resolve_combat(done_attacking_by_player, log, animations, game_state, 1 - attacking_player)


    def player_single_attack(self, 
                             attacking_player: int,
                             done_attacking_by_player: dict[int, bool], 
                             log: list[str],
                             animations: list,
                             game_state: 'GameState'):
        characters_that_can_attack = [character for character in self.characters_by_player[attacking_player] if character.can_attack()]            
        
        if len(characters_that_can_attack) == 0:
            done_attacking_by_player[attacking_player] = True
        else:
            characters_that_can_attack = [character for character in characters_that_can_attack if character.can_attack()]
            character = random.choice(characters_that_can_attack)
            defending_characters = [character for character in self.characters_by_player[1 - attacking_player] if character.can_fight()]
            character.attack(attacking_player, self.damage_by_player, defending_characters, self.lane_number, log, animations, game_state)

        dying_characters = [character for character in self.characters_by_player[0] + self.characters_by_player[1] if character.current_health <= 0]

        for dying_character in dying_characters:
            animations.append([{
                "event": "character_dies", 
                "dying_character_id": dying_character.id,
                "dying_character_lane_number": self.lane_number,
                "dying_character_player": dying_character.owner_number,
                "dying_character_index": [c.id for c in self.characters_by_player[dying_character.owner_number]].index(dying_character.id),
            }, game_state.to_json()])

            if dying_character.has_ability('SwitchLanesInsteadOfDying') and not dying_character.escaped_death:
                dying_character.escaped_death = True
                dying_character.switch_lanes(game_state)
                dying_character.fully_heal()

        for player_num in self.characters_by_player:
            self.characters_by_player[player_num] = [character for character in self.characters_by_player[player_num] if character.current_health > 0]


    def get_random_enemy_character(self, player_num: int) -> Optional[Character]:
        characters_available = [character for character in self.characters_by_player[1 - player_num] if character.can_fight()]
        return random.choice(characters_available) if len(characters_available) > 0 else None


    def to_json(self):
        return {
            "damage_by_player": self.damage_by_player.copy(),
            "characters_by_player": {player: [character.to_json() for character in self.characters_by_player[player]] for player in self.characters_by_player},
            "lane_number": self.lane_number,
        }

    @staticmethod
    def from_json(json):
        lane = Lane(json["lane_number"])
        lane.damage_by_player = json["damage_by_player"]
        lane.characters_by_player = {player: [Character.from_json(character, lane) for character in json["characters_by_player"][player]] for player in json["characters_by_player"]}
        return lane
