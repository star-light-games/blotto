from datetime import datetime
import random
from card_template import CardTemplate
from card_templates_list import CARD_TEMPLATES
from deck import Deck
from game_state_record import GameStateRecord
from lane import Lane
from card import Card
from typing import Any, Optional
import math

from utils import sigmoid


class GameState:
    def __init__(self, usernames_by_player: dict[int, str], decks_by_player: dict[int, Deck], lane_rewards: list[str]):
        self.lane_reward_names = lane_rewards
        self.lanes = [Lane(lane_number, lane_reward_str) for (lane_number, lane_reward_str) in zip(list(range(3)), lane_rewards)]
        self.turn = 0
        self.usernames_by_player = usernames_by_player
        self.player_0_hand, self.player_0_draw_pile = self.draw_initial_hand(decks_by_player[0])
        self.player_1_hand, self.player_1_draw_pile = self.draw_initial_hand(decks_by_player[1])
        self.hands_by_player = {0: self.player_0_hand, 1: self.player_1_hand}
        self.draw_piles_by_player = {0: self.player_0_draw_pile, 1: self.player_1_draw_pile}
        self.has_moved_by_player = {0: False, 1: False}
        self.has_mulliganed_by_player = {0: False, 1: False}
        self.done_with_animations_by_player = {0: False, 1: False}
        self.log: list[str] = []
        self.mana_by_player = {0: 0, 1: 0}
        self.decks_by_player = decks_by_player
        self.winner = None
        self.last_timer_start: Optional[float] = None
        self.roll_turn([])

    def draw_initial_hand(self, deck: Deck):
        draw_pile = deck.to_draw_pile()
        random.shuffle(draw_pile)
        hand = draw_pile[:3]
        draw_pile = draw_pile[3:]
        return hand, draw_pile

    def do_start_of_game(self, animations: list, seconds_per_turn: Optional[int] = None):
        for lane in self.lanes:
            lane.do_start_of_game(self.log, animations, self)

    def draw_card(self, player_num: int):
        if len(self.hands_by_player[player_num]) < 7:
            if len(self.draw_piles_by_player[player_num]) > 0:
                self.hands_by_player[player_num].append(self.draw_piles_by_player[player_num][0])
                self.draw_piles_by_player[player_num] = self.draw_piles_by_player[player_num][1:]
            else:
                self.log.append(f"{self.usernames_by_player[player_num]} has no cards left in their deck.")
        else:
            self.log.append(f"{self.usernames_by_player[player_num]} has a full hand.")
        self.run_card_draw_triggers(player_num)

    def draw_random_card(self, player_num: int):
        if len(self.hands_by_player[player_num]) < 7:
            random_template = random.choice([card_template for card_template in CARD_TEMPLATES.values() if not card_template.not_in_card_pool])
            self.hands_by_player[player_num].append(Card(random_template))
        else:
            self.log.append(f"{self.usernames_by_player[player_num]} has a full hand.")
        self.run_card_draw_triggers(player_num)

    def run_card_draw_triggers(self, player_num: int):
        for lane in self.lanes:
            for character in lane.characters_by_player[player_num]:
                if character.has_ability('OnDrawCardPump'):
                    character.current_attack += character.number_of_ability('OnDrawCardPump')
                    character.current_health += character.number_2_of_ability('OnDrawCardPump')
                    character.max_health += character.number_2_of_ability('OnDrawCardPump')

    def discard_card(self, player_num: int, card_id: str):
        self.hands_by_player[player_num] = [card for card in self.hands_by_player[player_num] if card.id != card_id]
        self.run_card_discard_triggers(player_num)

    def run_card_discard_triggers(self, player_num: int):
        for lane in self.lanes:
            for character in lane.characters_by_player[player_num]:
                if character.has_ability('OnDiscardPump'):
                    character.current_attack += character.number_of_ability('OnDiscardPump')
                    character.current_health += character.number_2_of_ability('OnDiscardPump')
                    character.max_health += character.number_2_of_ability('OnDiscardPump')

    def discard_all_cards(self, player_num: int):
        card_ids = [card.id for card in self.hands_by_player[player_num]]
        for card_id in card_ids:
            self.discard_card(player_num, card_id)

    def mulligan_all(self, player_num: int):
        if self.has_mulliganed_by_player[player_num]:
            return
        self.has_mulliganed_by_player[player_num] = True
        self.log.append(f"{self.usernames_by_player[player_num]} mulliganed their hand.")
        cards_in_hand = self.hands_by_player[player_num][:]
        for card in cards_in_hand:
            self.mulligan_card(player_num, card.id)

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

    def roll_turn(self, animations: list, sess: Optional[Any] = None, game_id: Optional[str] = None):
        if sess:
            game_state_record = GameStateRecord(
                game_id=game_id, 
                turn=self.turn,
                player_0_username=self.usernames_by_player[0],
                player_1_username=self.usernames_by_player[1],
                game_state=self.to_json(),
            )
            sess.add(game_state_record)
            sess.commit()

        self.turn += 1
        animations.clear()
        animations.append({
            'event_type': 'StartOfRoll',
            'data': {},
            'game_state': self.to_json(),
        })
        for player_num in [0, 1]:
            self.mana_by_player[player_num] = self.turn        
        for lane in self.lanes:
            lane.do_start_of_turn(self.log, animations, self)
        for lane in sorted(self.lanes, key=lambda lane: lane.lane_number + lane.additional_combat_priority):
            lane.roll_turn(self.log, animations, self)
        for lane in self.lanes:
            lane.do_end_of_turn(self.log, animations, self)
        animations.append({
                        "event_type": "EndOfRoll",
                        'data': {},
                        'game_state': self.to_json(),
                    })
                    
        for player_num in [0, 1]:
            self.draw_card(player_num)
        self.log.append(f"Turn {self.turn}")
        self.has_moved_by_player = {0: False, 1: False}
        self.done_with_animations_by_player = {0: False, 1: False}
        self.last_timer_start = None
        # if self.turn == 9:
        #     self.log.append("The moon rises.")
        #     self.mana_by_player = {0: 0, 1: 0}

        if self.turn == 9:
            self.log.append("The moon is full.")
            
            lane_winners = [lane.compute_winner() for lane in self.lanes]

            num_lanes_won_by_player = {player_num: sum([1 for lane_winner in lane_winners if lane_winner == player_num]) for player_num in [0, 1]}

            if num_lanes_won_by_player[0] > num_lanes_won_by_player[1]:
                self.log.append(f"{self.usernames_by_player[0]} won the game!")
                self.winner = 0

            if num_lanes_won_by_player[1] > num_lanes_won_by_player[0]:
                self.log.append(f"{self.usernames_by_player[1]} won the game!")
                self.winner = 1

            if num_lanes_won_by_player[0] == num_lanes_won_by_player[1]:
                total_damage_by_player = {player_num: sum([lane.damage_by_player[player_num] for lane in self.lanes]) for player_num in [0, 1]}
                if total_damage_by_player[0] > total_damage_by_player[1]:
                    self.log.append(f"{self.usernames_by_player[0]} won the game!")
                    self.winner = 0
                
                if total_damage_by_player[1] > total_damage_by_player[0]:
                    self.log.append(f"{self.usernames_by_player[1]} won the game!")
                    self.winner = 1

    def play_card(self, player_num: int, card_id: str, lane_number: int):
        if len(self.lanes[lane_number].characters_by_player[player_num]) < 4:
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

    def to_json(self):
        return {
            "lane_reward_names": self.lane_reward_names,
            "lanes": [lane.to_json() for lane in self.lanes],
            "turn": self.turn,
            "hands_by_player": {player_num: [card.to_json() for card in self.hands_by_player[player_num]] for player_num in self.hands_by_player},
            "draw_piles_by_player": {player_num: [card.to_json() for card in self.draw_piles_by_player[player_num]] for player_num in self.draw_piles_by_player},
            "log": self.log,
            "mana_by_player": self.mana_by_player,
            "has_moved_by_player": self.has_moved_by_player,
            "usernames_by_player": self.usernames_by_player,
            "decks_by_player": {k: v.to_json() for k, v in self.decks_by_player.items()},
            "has_mulliganed_by_player": self.has_mulliganed_by_player,
            "done_with_animations_by_player": self.done_with_animations_by_player,
            "winner": self.winner,
            "last_timer_start": self.last_timer_start,
        }
    
    @staticmethod
    def from_json(json):
        decks_by_player_json = {int(k): Deck.from_json(v) for k, v in json['decks_by_player'].items()} if json.get('decks_by_player') else {0: Deck([], '', ''), 1: Deck([], '', '')}
        game_state = GameState(json['usernames_by_player'], decks_by_player_json, json['lane_reward_names'])
        game_state.lanes = [Lane.from_json(lane_json) for lane_json in json['lanes']]
        game_state.turn = json['turn']
        game_state.hands_by_player = {int(player_num): [Card.from_json(card_json) for card_json in json['hands_by_player'][player_num]] for player_num in json['hands_by_player']}
        game_state.draw_piles_by_player = {int(player_num): [Card.from_json(card_json) for card_json in json['draw_piles_by_player'][player_num]] for player_num in json['draw_piles_by_player']} if json.get('draw_piles_by_player') else {0: [], 1: []}
        game_state.log = json.get('log') or []
        game_state.mana_by_player = {int(k): v for k, v in json['mana_by_player']}
        game_state.has_moved_by_player = {int(k): v for k, v in json['has_moved_by_player']}
        game_state.done_with_animations_by_player = {int(k): v for k, v in json['done_with_animations_by_player']}
        game_state.has_mulliganed_by_player = {int(k): v for k, v in json['has_mulliganed_by_player']}
        game_state.winner = json.get('winner')
        game_state.last_timer_start = json.get('last_timer_start')

        return game_state
    
    def copy(self):
        return GameState.from_json(self.to_json())