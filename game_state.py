import random
from card_template import CardTemplate
from card_templates_list import CARD_TEMPLATES
from deck import Deck
from lane import Lane
from card import Card
from typing import Optional
import math

from utils import sigmoid


class GameState:
    def __init__(self, usernames_by_player: dict[int, str], decks_by_player: dict[int, Deck]):
        self.lanes = [Lane(lane_number, lane_reward_str) for (lane_number, lane_reward_str) in zip(list(range(3)), ['Fire Nation', 'Southern Air Temple', 'Full Moon Bay'])]
        self.turn = 0        
        self.usernames_by_player = usernames_by_player
        self.player_0_hand, self.player_0_draw_pile = self.draw_initial_hand(decks_by_player[0])
        self.player_1_hand, self.player_1_draw_pile = self.draw_initial_hand(decks_by_player[1])
        self.hands_by_player = {0: self.player_0_hand, 1: self.player_1_hand}
        self.draw_piles_by_player = {0: self.player_0_draw_pile, 1: self.player_1_draw_pile}
        self.has_moved_by_player = {0: False, 1: False}
        self.has_mulliganed_by_player = {0: False, 1: False}
        self.log: list[str] = []
        self.animations: list = []
        self.mana_by_player = {0: 0, 1: 0}
        self.decks_by_player = decks_by_player
        self.roll_turn()

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
            self.log.append(f"{self.usernames_by_player[player_num]} has no cards left in their deck.")
        self.run_card_draw_triggers(player_num)

    def draw_random_card(self, player_num: int):
        random_template = random.choice([card_template for card_template in CARD_TEMPLATES.values() if not card_template.not_in_card_pool])
        self.hands_by_player[player_num].append(Card(random_template))
        self.run_card_draw_triggers(player_num)

    def run_card_draw_triggers(self, player_num: int):
        for lane in self.lanes:
            for character in lane.characters_by_player[player_num]:
                if character.has_ability('OnDrawCardPump'):
                    character.current_attack += character.number_of_ability('OnDrawCardPump')
                    character.current_health += character.number_2_of_ability('OnDrawCardPump')
                    character.max_health += character.number_2_of_ability('OnDrawCardPump')


    def mulligan_card(self, player_num: int, card_id: str):
        self.draw_piles_by_player[player_num].append([card for card in self.hands_by_player[player_num] if card.id == card_id][0])
        self.hands_by_player[player_num] = [card for card in self.hands_by_player[player_num] if card.id != card_id]
        self.log.append(f"{self.usernames_by_player[player_num]} mulliganed a card.")
        self.draw_card(player_num)

    def mulligan_cards(self, player_num: int, cards: list[str]):
        if self.has_mulliganed_by_player[player_num]:
            return   
        cards = cards[:]   
        random.shuffle(cards)  
        for card_id in cards:
            self.mulligan_card(player_num, card_id)
        self.has_mulliganed_by_player[player_num] = True

    def roll_turn(self):
        self.turn += 1
        self.animations = [[{"event": "start_of_roll"}, self.to_json()]]
        for player_num in [0, 1]:
            self.mana_by_player[player_num] = self.turn        
        for lane in self.lanes:
            lane.do_start_of_turn(self.log, self.animations, self)
        for lane in sorted(self.lanes, key=lambda lane: lane.lane_number + lane.additional_combat_priority):
            lane.roll_turn(self.log, self.animations, self)
        for lane in self.lanes:
            lane.do_end_of_turn(self.log, self.animations, self)
        self.animations.append([{
                        "event_type": "end_of_roll",
                    }, self.to_json()])
                    
        for player_num in [0, 1]:
            self.draw_card(player_num)
        self.log.append(f"Turn {self.turn}")
        self.has_moved_by_player = {0: False, 1: False}
        if self.turn == 9:
            self.log.append("The moon rises.")
            self.mana_by_player = {0: 0, 1: 0}

    def play_card(self, player_num: int, card_id: str, lane_number: int):
        card = [card for card in self.hands_by_player[player_num] if card.id == card_id][0]
        self.hands_by_player[player_num] = [card for card in self.hands_by_player[player_num] if card.id != card_id]
        character = card.to_character(self.lanes[lane_number], player_num, self.usernames_by_player[player_num])
        self.lanes[lane_number].characters_by_player[player_num].append(character)
        self.log.append(f"{self.usernames_by_player[player_num]} played {card.template.name} in Lane {lane_number + 1}.")

    # Should be used only by bots
    def play_card_from_template(self, player_num: int, card_template: CardTemplate, lane_number: int):
        card = Card(card_template)
        character = card.to_character(self.lanes[lane_number], player_num, self.usernames_by_player[player_num])
        self.lanes[lane_number].characters_by_player[player_num].append(character)
        self.log.append(f"{self.usernames_by_player[player_num]} played {card_template.name} in Lane {lane_number + 1}.")

    def all_players_have_moved(self) -> bool:
        return all([self.has_moved_by_player[player_num] for player_num in [0, 1]])

    def find_random_empty_slot_in_other_lane(self, not_in_lane_num: int, player_num: int) -> Optional[Lane]:
        other_lane_numbers = [lane_number for lane_number in [0, 1, 2] if lane_number != not_in_lane_num]
        empty_slots_by_lane_number_in_other_lanes = {lane_number: max(4 - len(self.lanes[lane_number].characters_by_player[player_num]), 0) for lane_number in other_lane_numbers}
        total_empty_slots = sum(empty_slots_by_lane_number_in_other_lanes.values())
        if total_empty_slots == 0:
            return None
        probability_of_moving_to_first_other_lane = empty_slots_by_lane_number_in_other_lanes[other_lane_numbers[0]] / total_empty_slots

        if random.random() < probability_of_moving_to_first_other_lane:
            target_lane_number = other_lane_numbers[0]
        else:
            target_lane_number = other_lane_numbers[1]

        target_lane = self.lanes[target_lane_number]
        return target_lane

    def get_random_lane_with_empty_slot(self, player_num: int) -> Optional[int]:
        lanes_with_empty_slots = [lane_number for lane_number in [0, 1, 2] if len(self.lanes[lane_number].characters_by_player[player_num]) < 4]
        if lanes_with_empty_slots == []:
            return None
        return random.choice(lanes_with_empty_slots)    

    def to_json(self, exclude_animations: bool = True):
        return {
            "lanes": [lane.to_json() for lane in self.lanes],
            "turn": self.turn,
            "hands_by_player": {player_num: [card.to_json() for card in self.hands_by_player[player_num]] for player_num in self.hands_by_player},
            "draw_piles_by_player": {player_num: [card.to_json() for card in self.draw_piles_by_player[player_num]] for player_num in self.draw_piles_by_player},
            "log": self.log[:],
            "mana_by_player": self.mana_by_player,
            "has_moved_by_player": self.has_moved_by_player,
            "usernames_by_player": self.usernames_by_player,
            "decks_by_player": {k: v.to_json() for k, v in self.decks_by_player.items()},
            **({"animations": self.animations} if not exclude_animations else {}),
            "has_mulliganed_by_player": self.has_mulliganed_by_player
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
        if json.get('animations'):
            game_state.animations = json['animations']
        game_state.has_mulliganed_by_player = json['has_mulliganed_by_player']

        return game_state
    
    def copy(self):
        return GameState.from_json(self.to_json())