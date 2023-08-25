import random
from deck import Deck
from lane import Lane
from card import Card


class GameState:
    def __init__(self, usernames_by_player: dict[int, str], decks_by_player: dict[int, Deck]):
        self.lanes = [Lane(lane_number) for lane_number in range(3)]
        self.turn = 0        
        self.usernames_by_player = usernames_by_player
        self.player_0_hand, self.player_0_draw_pile = self.draw_initial_hand(decks_by_player[0])
        self.player_1_hand, self.player_1_draw_pile = self.draw_initial_hand(decks_by_player[1])
        self.hands_by_player = {0: self.player_0_hand, 1: self.player_1_hand}
        self.draw_piles_by_player = {0: self.player_0_draw_pile, 1: self.player_1_draw_pile}
        self.has_moved_by_player = {0: False, 1: False}
        self.log: list[str] = []
        self.mana_by_player = {0: 0, 1: 0}
        self.decks_by_player = decks_by_player
        self.roll_turn()

    def draw_initial_hand(self, deck: Deck):
        draw_pile = deck.to_draw_pile()
        random.shuffle(draw_pile)
        hand = draw_pile[:2]
        draw_pile = draw_pile[2:]
        return hand, draw_pile

    def draw_card(self, player_num: int):
        if len(self.draw_piles_by_player[player_num]) > 0:
            self.hands_by_player[player_num].append(self.draw_piles_by_player[player_num][0])
            self.draw_piles_by_player[player_num] = self.draw_piles_by_player[player_num][1:]
        else:
            self.log.append(f"{self.usernames_by_player[player_num]} has no cards left in their deck.")

    def roll_turn(self):
        self.turn += 1
        for lane in self.lanes:
            lane.roll_turn(self.log)
        for player_num in [0, 1]:
            self.draw_card(player_num)
        self.log.append(f"Turn {self.turn}")
        for player_num in [0, 1]:
            self.mana_by_player[player_num] = self.turn
        self.has_moved_by_player = {0: False, 1: False}

    def play_card(self, player_num: int, card_id: str, lane_number: int):
        card = [card for card in self.hands_by_player[player_num] if card.id == card_id][0]
        self.hands_by_player[player_num] = [card for card in self.hands_by_player[player_num] if card.id != card_id]
        character = card.to_character(self.lanes[lane_number], player_num, self.usernames_by_player[player_num])
        self.lanes[lane_number].characters_by_player[player_num].append(character)
        self.log.append(f"{self.usernames_by_player[player_num]} played {card.template.name} in Lane {lane_number + 1}.")

    def all_players_have_moved(self) -> bool:
        return all([self.has_moved_by_player[player_num] for player_num in [0, 1]])

    def to_json(self):
        return {
            "lanes": [lane.to_json() for lane in self.lanes],
            "turn": self.turn,
            "hands_by_player": {player_num: [card.to_json() for card in self.hands_by_player[player_num]] for player_num in self.hands_by_player},
            "draw_piles_by_player": {player_num: [card.to_json() for card in self.draw_piles_by_player[player_num]] for player_num in self.draw_piles_by_player},
            "log": self.log,
            "mana_by_player": self.mana_by_player,
            "has_moved_by_player": self.has_moved_by_player,
            "usernames_by_player": self.usernames_by_player,
            "decks_by_player": {k: v.to_json() for k, v in self.decks_by_player.items()},
        }
    
    @staticmethod
    def from_json(json):
        game_state = GameState(json['usernames_by_player'], {k: Deck.from_json(v) for k, v in json['decks_by_player'].items()})
        game_state.lanes = [Lane.from_json(lane_json) for lane_json in json['lanes']]
        game_state.turn = json['turn']
        game_state.hands_by_player = {player_num: [Card.from_json(card_json) for card_json in json['hands_by_player'][player_num]] for player_num in json['hands_by_player']}
        game_state.draw_piles_by_player = {player_num: [Card.from_json(card_json) for card_json in json['draw_piles_by_player'][player_num]] for player_num in json['draw_piles_by_player']}
        game_state.log = json['log']
        game_state.mana_by_player = json['mana_by_player']
        game_state.has_moved_by_player = json['has_moved_by_player']

        return game_state