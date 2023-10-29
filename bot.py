import random
import traceback
from typing import Optional
from card_templates_list import CARD_TEMPLATES
from common_decks import BOT_DRAFT_DECKS, COMMON_DECKS
from db_deck import DbDeck
from deck import Deck
from game import Game
from game_state import GameState
from redis_utils import rdel, rget_json, rlock, rset_json
from settings import BOT_DECK_USERNAME, COMMON_DECK_USERNAME
from utils import get_game_lock_redis_key, get_game_redis_key, get_game_with_hidden_information_redis_key, run_with_timeout, sigmoid
from sqlalchemy import func, not_
import logging

logger = logging.getLogger(__name__)


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

def get_bot_deck(sess, player_deck_name: str) -> Optional[Deck]:
    from common_decks import COMMON_DECKS, BOT_DRAFT_DECKS
    from deck import Deck
    if player_deck_name == 'Learn to play':
        return Deck.from_db_deck(db_deck) if (db_deck := sess.query(DbDeck).filter(DbDeck.name == 'Learn to play').filter(DbDeck.username == COMMON_DECK_USERNAME).first()) else None
    elif player_deck_name in [common_deck['name'] for common_deck in COMMON_DECKS]:
        return Deck.from_db_deck(db_deck) if (db_deck := sess.query(DbDeck).filter(not_(DbDeck.name.in_(['Learn to play', player_deck_name]))).filter(DbDeck.username == COMMON_DECK_USERNAME).order_by(func.random()).first()) else None
    elif 'Draft deck' in player_deck_name:
        return Deck.from_db_deck(db_deck) if (db_deck := sess.query(DbDeck).filter(DbDeck.username == BOT_DECK_USERNAME).order_by(func.random()).first()) else None
    else:
        return Deck.from_db_deck(db_deck) if (db_deck := sess.query(DbDeck).filter(DbDeck.name != 'Learn to play').filter(DbDeck.username == COMMON_DECK_USERNAME).order_by(func.random()).first()) else None
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

        game_state.roll_turn([])

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
    NUM_RANDOM_GAMES = 7
    total_probability = 0.0
    for _ in range(NUM_RANDOM_GAMES):
        total_probability += assess_final_position(player_num, randomly_play_forward_game_state_with_mana_amounts(mana_amounts_by_player, game_state))
    return total_probability


def find_bot_move(bot_username: str, player_num: int, game: Game) -> dict[str, int]:
    assert game.game_info

    if game.seconds_per_turn is None:
        time_to_think = 10
    else:
        time_to_think = min(10, game.seconds_per_turn - 1)

    if bot_username == 'RANDY_THE_ROBOT':
        return find_bot_move_randy(player_num, game.game_info.game_state)
    
    elif bot_username == 'RUFUS_THE_ROBOT':
        try:
            rufus_move = run_with_timeout(find_bot_move_rufus, time_to_think, player_num, game.game_info.game_state)
        except Exception as e:
            logger.error(f'Error in find_bot_move_rufus in game {game.id} on turn {game.game_info.game_state.turn}: {e}')
            logger.error(traceback.print_exc())
            rufus_move = None
        else:
            if rufus_move is None:
                logger.warning(f'Rufus timed out in game {game.id} on turn {game.game_info.game_state.turn}')
            else:
                logger.info(f'Rufus played turn {game.game_info.game_state.turn} of game {game.id} without issues: {rufus_move}')

        if rufus_move is None:
            return find_bot_move_randy(player_num, game.game_info.game_state)
        return rufus_move
    
    return {}


def find_bot_move_randy(player_num: int, game_state: GameState) -> dict[str, int]:

    cards_in_hand = game_state.hands_by_player[player_num]

    # Stores dict of mana one could spend to a tuple of (mana actually spent, # cards in each lane, card id to lane number)
    num_cards_in_each_lane = [len(game_state.lanes[lane_number].characters_by_player[player_num]) for lane_number in [0, 1, 2]]
    best_move_spending_x_mana: dict[int, tuple[int, list[int], dict[str, int]]] = {0: (0, num_cards_in_each_lane, {})}

    for x in range(1, game_state.mana_by_player[player_num] + 1):
        best_move_spending_x_mana[x] = best_move_spending_x_mana[x-1]
        best_mana_spent = best_move_spending_x_mana[x-1][0]
        for card in cards_in_hand:
            if card.template.cost <= x:
                best_move_spending_x_mana_tup = best_move_spending_x_mana[x - card.template.cost]
                num_cards_in_each_lane_in_this_scenario = best_move_spending_x_mana_tup[1][:]
                mana_spent_playing_that_card = best_move_spending_x_mana_tup[0] + card.template.cost

                if mana_spent_playing_that_card > best_mana_spent:
                    best_mana_spent = mana_spent_playing_that_card

                    playable_lanes = [lane_number for lane_number in [0, 1, 2] if num_cards_in_each_lane_in_this_scenario[0] < 4]
                    if len(playable_lanes) > 0:
                        lane_number = random.choice(playable_lanes)
                        num_cards_in_each_lane_in_this_scenario[lane_number] += 1
                        best_move_spending_x_mana[x] = (best_mana_spent, num_cards_in_each_lane_in_this_scenario, {**best_move_spending_x_mana_tup[2], card.id: lane_number})

    return best_move_spending_x_mana[game_state.mana_by_player[player_num]][2]


def find_bot_move_rufus(player_num: int, game_state: GameState) -> dict[str, int]:
    cards_in_hand = game_state.hands_by_player[player_num][:5]

    logger.debug(f'My cards: {[card.to_json() for card in cards_in_hand]}')
    # Stores dict of mana spent to a tuple of (best game state, card id to lane number)
    best_game_state_spending_x_mana = {0: (game_state.copy(), {})}
    for x in range(1, game_state.mana_by_player[player_num] + 1):
        logger.debug(f'Trying to find the best move in the position that spends {x} mana.')
        mana_amounts_by_player = game_state.mana_by_player.copy()
        mana_amounts_by_player[player_num] -= x
        best_probability_so_far = assess_intermediate_position(player_num, mana_amounts_by_player, game_state)
        logger.debug(f'My assessment of the base position: {best_probability_so_far}')
        best_game_state_spending_x_mana[x] = (best_game_state_spending_x_mana[x-1][0], best_game_state_spending_x_mana[x-1][1].copy())
        for card in cards_in_hand:
            if card.template.cost <= x:
                logger.debug(f'Considering playing card {card.template.name}, {card.to_json()}')
                best_game_state_playing_that_card = best_game_state_spending_x_mana[x - card.template.cost][0].copy()
                cards_played = best_game_state_spending_x_mana[x - card.template.cost][1]
                logger.debug(f'Here are the cards in my hand in this scenario: {[card.to_json() for card in best_game_state_playing_that_card.hands_by_player[player_num]]}')
                if card.id in [c.id for c in best_game_state_playing_that_card.hands_by_player[player_num]]:
                    for lane_number in [0, 1, 2]:
                        if len(best_game_state_playing_that_card.lanes[lane_number].characters_by_player[player_num]) < 4:
                            best_game_state_playing_that_card_copy = best_game_state_playing_that_card.copy()
                            best_game_state_playing_that_card_copy.play_card(player_num, card.id, lane_number)
                            logger.debug(f'Trying to play card: {card.to_json()} in lane: {lane_number}')
                            probability_of_winning = assess_intermediate_position(player_num, mana_amounts_by_player, best_game_state_playing_that_card_copy)
                            logger.debug(f'My assessment of the resulting position: {probability_of_winning}')

                            if probability_of_winning > best_probability_so_far:
                                new_cards_played = cards_played.copy()
                                new_cards_played[card.id] = lane_number
                                best_game_state_spending_x_mana[x] = (best_game_state_playing_that_card_copy, new_cards_played)
                                best_probability_so_far = probability_of_winning

        logger.debug(f'I think the best move that spends {x} mana is: {best_game_state_spending_x_mana[x][1]}')

    return best_game_state_spending_x_mana[game_state.mana_by_player[player_num]][1]


def bot_take_mulligan(game_state: GameState, player_num: int) -> None:
    cards_in_hand = game_state.hands_by_player[player_num]
    logger.debug(f'My cards: {[card.template.name for card in cards_in_hand]}')

    game_state.has_mulliganed_by_player[player_num] = True

    if all([card.template.cost > 2 for card in cards_in_hand]):
        # Mulligan everything if I have no one or two drops
        logger.debug('Pitching all cards; I have no one or two drops')
        # return game_state.mulligan_cards(player_num, [card.id for card in cards_in_hand])
        return game_state.mulligan_all(player_num)

    # else:
    #     # Mulligan all four and five drops
    #     print('Pitching the following cards: ', [card.template.name for card in cards_in_hand if card.template.cost >= 4])
    #     return game_state.mulligan_cards(player_num, [card.id for card in cards_in_hand if card.template.cost >= 4])
