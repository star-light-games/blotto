from typing import Optional
from card_templates_list import CARD_TEMPLATES
from deck import Deck
from game_state import GameState
from redis_utils import rget_json
from utils import sigmoid


RANDOM_CARDS_TO_PLAY = {
    1: ['generic_1drop'],
    2: ['generic_2drop'],
    3: ['generic_3drop'],
    4: ['generic_4drop'],
    5: ['generic_4drop', 'generic_1drop'],
    6: ['generic_4drop', 'generic_2drop'],
    7: ['generic_4drop', 'generic_3drop'],
    8: ['generic_4drop', 'generic_4drop'],
    9: ['generic_4drop', 'generic_4drop', 'generic_1drop'],
    10: ['generic_4drop', 'generic_4drop', 'generic_2drop'],
    11: ['generic_4drop', 'generic_4drop', 'generic_3drop'],
    12: ['generic_4drop', 'generic_4drop', 'generic_4drop'],
}

def get_bot_deck() -> Optional[Deck]:
    decks = rget_json('decks') or {}
    for deck_json in decks.values():
        deck = Deck.from_json(deck_json)
        if deck.name == 'Learn to play':
            return deck

    return None


def get_random_play(mana_amount: int) -> list[str]:
    if mana_amount < 1:
        return []
    elif mana_amount > 12:
        return ['generic_4drop', 'generic_4drop', 'generic_4drop']
    else:
        return RANDOM_CARDS_TO_PLAY[mana_amount]
    

def randomly_play_forward_game_state_with_mana_amounts(mana_amounts_by_player: dict[int, int], game_state: GameState) -> GameState:
    game_state = game_state.copy()
    mana_amounts_by_player_copy = mana_amounts_by_player.copy()
    game_state.mana_by_player = mana_amounts_by_player_copy

    while game_state.turn < 10:
        for player_num in [0, 1]:
            for card_name in get_random_play(mana_amounts_by_player_copy[player_num]):
                lane_number = game_state.get_random_lane_with_empty_slot(player_num)
                if lane_number is not None:
                    game_state.play_card_from_template(player_num, CARD_TEMPLATES[card_name], lane_number)

        game_state.roll_turn()

    return game_state


def assess_final_position(player_num: int, game_state: GameState) -> float:
    CHARACTERISTIC_TOWER_HEALTH_AMOUNT = 20
    probability_of_winning_each_lane = [sigmoid((lane.damage_by_player[0] - lane.damage_by_player[1]) / CHARACTERISTIC_TOWER_HEALTH_AMOUNT) for lane in game_state.lanes]
    probability_of_winning_game = (
        probability_of_winning_each_lane[0] * probability_of_winning_each_lane[1] * (1 - probability_of_winning_each_lane[2]) +
        probability_of_winning_each_lane[0] * (1 - probability_of_winning_each_lane[1]) * probability_of_winning_each_lane[2] +
        (1 - probability_of_winning_each_lane[0]) * probability_of_winning_each_lane[1] * probability_of_winning_each_lane[2] +
        probability_of_winning_each_lane[0] * probability_of_winning_each_lane[1] * probability_of_winning_each_lane[2]
    )

    if player_num == 0:
        return probability_of_winning_game
    else:
        return 1 - probability_of_winning_game


def assess_intermediate_position(player_num: int, mana_amounts_by_player: dict[int, int], game_state: GameState) -> float:
    NUM_RANDOM_GAMES = 30
    total_probability = 0.0
    for _ in range(NUM_RANDOM_GAMES):
        total_probability += assess_final_position(player_num, randomly_play_forward_game_state_with_mana_amounts(mana_amounts_by_player, game_state))
    return total_probability


def find_bot_move(player_num: int, game_state: GameState) -> dict[str, int]:
    cards_in_hand = game_state.hands_by_player[player_num]
    # Stores dict of mana spent to a tuple of (best game state, card id to lane number)
    best_game_state_spending_x_mana = {0: (game_state.copy(), {})}
    for x in range(1, game_state.mana_by_player[player_num] + 1):
        mana_amounts_by_player = game_state.mana_by_player.copy()
        mana_amounts_by_player[player_num] -= x
        best_probability_so_far = assess_intermediate_position(player_num, mana_amounts_by_player, game_state)
        best_game_state_spending_x_mana[x] = (best_game_state_spending_x_mana[x-1][0], best_game_state_spending_x_mana[x-1][1].copy())
        for card in cards_in_hand:
            if card.template.cost <= x:
                best_game_state_playing_that_card = best_game_state_spending_x_mana[card.template.cost][0].copy()
                cards_played = best_game_state_spending_x_mana[card.template.cost][1]
                if not card.id in cards_played:
                    for lane_number in [0, 1, 2]:
                        if len(best_game_state_playing_that_card.lanes[lane_number].characters_by_player[player_num]) < 4:
                            best_game_state_playing_that_card.play_card(player_num, card.id, lane_number)
                            probability_of_winning = assess_intermediate_position(player_num, mana_amounts_by_player, best_game_state_playing_that_card)

                            if probability_of_winning > best_probability_so_far:
                                new_cards_played = cards_played.copy()
                                new_cards_played[card.id] = lane_number
                                best_game_state_spending_x_mana[x] = (best_game_state_playing_that_card, new_cards_played)
                                best_probability_so_far = probability_of_winning

    return best_game_state_spending_x_mana[game_state.mana_by_player[player_num]][1]

