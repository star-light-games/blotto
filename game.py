from deck import Deck
from game_state import GameState
from lane import Lane
from utils import generate_unique_id
from typing import Optional


class Game:
    def __init__(self, usernames_by_player: dict[int, Optional[str]], decks_by_player: dict[int, Optional[Deck]]):
        self.id = generate_unique_id()
        self.usernames_by_player = usernames_by_player
        self.decks_by_player = decks_by_player
        self.game_state = None


    def start(self):
        assert all([username is not None for username in self.usernames_by_player.values()])
        assert all([deck is not None for deck in self.decks_by_player.values()])

        self.game_state = GameState(self.usernames_by_player, self.decks_by_player)  # type: ignore


    def to_json(self):
        return {
            "id": self.id,
            "usernames_by_player": self.usernames_by_player,
            "game_state": self.game_state.to_json() if self.game_state is not None else None,
        }