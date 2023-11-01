from game_state import GameState


class GameInfo:
    def __init__(self, game_state: GameState) -> None:
        self.animations = []
        self.game_state = game_state

    def to_json(self) -> dict:
        return {
            "animations": self.animations,
            "game_state": self.game_state.to_json() if self.game_state is not None else None,
        }
    
    def do_start_of_game(self):
        self.game_state.do_start_of_game(self.animations)

    def roll_turn(self, sess, game_id: str):
        self.game_state.roll_turn(self.animations, sess, game_id, self)

    @staticmethod
    def from_json(json: dict) -> 'GameInfo':
        game_info = GameInfo(GameState.from_json(json['game_state']))
        game_info.animations = json['animations']
        return game_info