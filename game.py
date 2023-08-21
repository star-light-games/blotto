from deck import Deck
from game_state import GameState
from lane import Lane
from utils import generate_unique_id


class Game:
    def __init__(self, usernames_by_player: dict[int, str], decks_by_player: dict[int, Deck]):
        self.id = generate_unique_id()
        self.usernames_by_player = usernames_by_player
        self.decks_by_player = decks_by_player
        self.game_state = GameState(usernames_by_player, decks_by_player)


    def to_json(self):
        return {
            "id": self.id,
            "player_1_username": self.player_1_username,
            "player_2_username": self.player_2_username,
            "game_state": self.game_state.to_json(),
        }