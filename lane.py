from typing import TYPE_CHECKING
import random
from typing import Optional
from card_templates_list import CARD_TEMPLATES
from character import Character
from lane_rewards import LANE_REWARDS, LaneReward
from utils import shuffled
if TYPE_CHECKING:
    from game_state import GameState


class Lane:
    def __init__(self, lane_number: int, lane_reward_str: str):
        self.damage_by_player: dict[int, int] = {0: 0, 1: 0}
        self.characters_by_player: dict[int, list[Character]] = {0: [], 1: []}
        self.lane_number = lane_number
        self.additional_combat_priority = 0
        self.lane_reward = LaneReward.from_json(LANE_REWARDS[lane_reward_str])
        self.earned_rewards_by_player: dict[int, bool] = {0: False, 1: False}


    def maybe_give_lane_reward(self, player_num: int, game_state: 'GameState') -> None:
        if not self.earned_rewards_by_player[player_num] and self.damage_by_player[player_num] >= self.lane_reward.threshold:
            self.give_lane_reward(player_num, game_state)
            self.earned_rewards_by_player[player_num] = True


    def give_lane_reward(self, player_num: int, game_state: 'GameState') -> None:
        if self.lane_reward.name == 'Fire Nation':
            for lane in game_state.lanes:
                for character in lane.characters_by_player[player_num]:
                    character.current_attack += 3
        elif self.lane_reward.name == 'Southern Air Temple':
            lane_to_spawn_in = game_state.find_random_empty_slot_in_other_lane(self.lane_number, player_num)
            if lane_to_spawn_in is not None:
                lane_to_spawn_in.characters_by_player[player_num].append(Character(CARD_TEMPLATES['Air Nomads'], lane_to_spawn_in, player_num, game_state.usernames_by_player[player_num]))
        elif self.lane_reward.name == 'Full Moon Bay':
            game_state.draw_card(player_num)


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

            was_saved = False
            for lane in shuffled([lane for lane in game_state.lanes if not lane.lane_number == self.lane_number]):
                for character in lane.characters_by_player[dying_character.owner_number]:
                    if character.has_ability('OnFriendlyCharacterDeathHealFullyAndSwitchLanes'):
                        if dying_character.switch_lanes(game_state, lane_number=lane.lane_number, and_fully_heal_if_switching=True):
                            was_saved = True
                        

            if dying_character.has_ability('SwitchLanesInsteadOfDying') and not dying_character.escaped_death and not was_saved:
                if dying_character.switch_lanes(game_state, and_fully_heal_if_switching=True):
                    dying_character.escaped_death = True      
                

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
            "lane_reward": self.lane_reward.to_json(),
            "earned_rewards_by_player": self.earned_rewards_by_player.copy(),
        }

    @staticmethod
    def from_json(json):
        lane = Lane(json["lane_number"], json["lane_reward"]["name"])
        lane.damage_by_player = json["damage_by_player"]
        lane.characters_by_player = {player: [Character.from_json(character, lane) for character in json["characters_by_player"][player]] for player in json["characters_by_player"]}
        lane.earned_rewards_by_player = json["earned_rewards_by_player"]
        return lane
