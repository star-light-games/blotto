from deck import Deck
from game_state import GameState
from lane import Lane
from utils import generate_unique_id
from typing import Optional
from datetime import datetime


class Game:
    def __init__(self, usernames_by_player: dict[int, Optional[str]], decks_by_player: dict[int, Optional[Deck]], id: Optional[str] = None):
        self.id = id if id is not None else generate_unique_id()
        self.usernames_by_player = usernames_by_player
        self.decks_by_player = decks_by_player
        self.game_state = None
        self.created_at = datetime.now().timestamp()
        self.rematch_game_id = None
        self.is_bot_by_player = {0: False, 1: False}


    def start(self):
        assert all([username is not None for username in self.usernames_by_player.values()])
        assert all([deck is not None for deck in self.decks_by_player.values()])

        self.game_state = GameState(self.usernames_by_player, self.decks_by_player)  # type: ignore
        self.rematch_game_id = generate_unique_id()


    def username_to_player_num(self, username: str) -> Optional[int]:
        return next((player_num for player_num, player_username in self.usernames_by_player.items() if player_username == username), None)


    def to_json(self):
        return {
            "id": self.id,
            "usernames_by_player": self.usernames_by_player,
            "decks_by_player": {k: v.to_json() if v is not None else None for k, v in self.decks_by_player.items()},
            "game_state": self.game_state.to_json(exclude_animations=False) if self.game_state is not None else None,
            "created_at": self.created_at,
            "rematch_game_id": self.rematch_game_id,
        }
    

    @staticmethod
    def from_json(json):
        game = Game(json['usernames_by_player'], {k: Deck.from_json(v) if v is not None else None for k, v in json['decks_by_player'].items()})
        game.id = json['id']
        game.game_state = GameState.from_json(json['game_state']) if json['game_state'] is not None else None
        game.created_at = json['created_at']
        game.rematch_game_id = json['rematch_game_id']
        return game

