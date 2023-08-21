import random
from deck import Deck
from lane import Lane


class GameState:
    def __init__(self, usernames_by_player: dict[int, str], decks_by_player: dict[int, Deck]):
        self.lanes = [Lane(lane_number) for lane_number in range(3)]
        self.turn = 0        
        self.usernames_by_player = usernames_by_player
        self.player_0_hand, self.player_0_draw_pile = self.draw_initial_hand(decks_by_player[0])
        self.player_1_hand, self.player_1_draw_pile = self.draw_initial_hand(decks_by_player[1])
        self.hands_by_player = {0: self.player_0_hand, 1: self.player_1_hand}
        self.draw_piles_by_player = {0: self.player_0_draw_pile, 1: self.player_1_draw_pile}
        self.log: list[str] = []

    def draw_initial_hand(self, deck: Deck):
        draw_pile = deck.to_draw_pile()
        random.shuffle(draw_pile)
        hand = draw_pile[:3]
        draw_pile = draw_pile[3:]
        return hand, draw_pile

    def draw_card(self, player_num: int):
        if len(self.draw_piles_by_player[player_num]) > 0:
            self.hands_by_player[player_num].append(self.draw_piles_by_player[player_num][0])
            self.draw_piles_by_player[player_num] = self.draw_piles_by_player[player_num][1:]
        else:
            self.log.append(f"Player {player_num + 1} has no cards left in their deck")

    def roll_turn(self):
        self.turn += 1
        for lane in self.lanes:
            lane.roll_turn(self.log)
        for player_num in [0, 1]:
            self.draw_card(player_num)
        self.log.append(f"Turn {self.turn}")



    def to_json(self):
        return {
            "lanes": [lane.to_json() for lane in self.lanes],
            "turn": self.turn,
            "hands_by_player": {player_num: [card.to_json() for card in self.hands_by_player[player_num]] for player_num in self.hands_by_player},
            "draw_piles_by_player": {player_num: [card.to_json() for card in self.draw_piles_by_player[player_num]] for player_num in self.draw_piles_by_player},
            "log": self.log,
        }