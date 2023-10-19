import random
from deck import Deck
from game_state import GameState
from lane import Lane
from lane_rewards import LANE_REWARDS
from utils import generate_unique_id
from typing import Optional
from datetime import datetime
from game_info import GameInfo


class Game:
    def __init__(self, 
                 usernames_by_player: dict[int, Optional[str]], 
                 decks_by_player: dict[int, Optional[Deck]], 
                 seconds_per_turn: Optional[int] = None, 
                 id: Optional[str] = None):
        self.id = id if id is not None else generate_unique_id()
        self.usernames_by_player = usernames_by_player
        self.decks_by_player = decks_by_player
        self.game_info: Optional[GameInfo] = None
        self.created_at = datetime.now().timestamp()
        self.rematch_game_id = None
        self.is_bot_by_player = {0: False, 1: False}
        self.seconds_per_turn = seconds_per_turn


    def start(self):
        assert all([username is not None for username in self.usernames_by_player.values()])
        assert all([deck is not None for deck in self.decks_by_player.values()])

        if any([deck.name == 'Learn to play' for deck in self.decks_by_player.values()]):  # type: ignore
            lane_reward_names = ['Fire Nation', 'Southern Air Temple', 'Full Moon Bay']
        else:
            lanes_from_decks = set([deck.associated_lane_reward_name for deck in self.decks_by_player.values() if deck.associated_lane_reward_name is not None])  # type: ignore
            random_lanes = random.sample([lane_reward['name'] for lane_reward in LANE_REWARDS.values() if lane_reward['name'] not in lanes_from_decks], 3 - len(lanes_from_decks))
            lane_reward_names = [*lanes_from_decks, *random_lanes]
            lane_reward_names.sort(key=lambda lane_reward_name: LANE_REWARDS[lane_reward_name]['priority'])        

        game_state = GameState(self.usernames_by_player, self.decks_by_player, lane_reward_names)  # type: ignore
        self.game_info = GameInfo(game_state)
        self.game_info.do_start_of_game()
        self.rematch_game_id = generate_unique_id()

        print(f'game_info: {self.game_info}')


    def all_players_are_done_with_animations(self) -> bool:
        assert self.game_info is not None
        return all([self.game_info.game_state.done_with_animations_by_player[player_num] or self.is_bot_by_player[player_num] for player_num in [0, 1]])


    def username_to_player_num(self, username: str) -> Optional[int]:
        return next((player_num for player_num, player_username in self.usernames_by_player.items() if player_username == username), None)


    def to_json(self):
        return {
            "id": self.id,
            "usernames_by_player": self.usernames_by_player,
            "decks_by_player": {k: v.to_json() if v is not None else None for k, v in self.decks_by_player.items()},
            "game_info": self.game_info.to_json() if self.game_info is not None else None,
            "created_at": self.created_at,
            "rematch_game_id": self.rematch_game_id,
            "is_bot_by_player": self.is_bot_by_player,
            "seconds_per_turn": self.seconds_per_turn,
        }
    

    @staticmethod
    def from_json(json):
        game = Game(json['usernames_by_player'], 
                    {k: Deck.from_json(v) if v is not None else None for k, v in json['decks_by_player'].items()},
                    json.get('seconds_per_turn'),)
        game.id = json['id']
        game.game_info = GameInfo.from_json(json['game_info']) if json['game_info'] is not None else None
        game.created_at = json['created_at']
        game.rematch_game_id = json['rematch_game_id']
        game.is_bot_by_player = json['is_bot_by_player']
        return game

