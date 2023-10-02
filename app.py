#!/usr/bin/python3

from datetime import datetime, timedelta
from bot import bot_take_mulligan, find_bot_move, get_bot_deck
from card_templates_list import CARD_TEMPLATES
from common_decks import create_common_decks
from deck import Deck
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS
from game import Game
import traceback
from functools import wraps
import random
from _thread import start_new_thread
from lane_rewards import LANE_REWARDS

from redis_utils import rdel, rget_json, rlock, rset_json
from settings import COMMON_DECK_USERNAME, LOCAL
from utils import generate_unique_id, get_game_lock_redis_key, get_game_redis_key, get_game_with_hidden_information_redis_key


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


def bot_move_in_game(game: Game, player_num: int) -> None:
    assert game.game_state 
    bot_move = find_bot_move(player_num, game.game_state)
    print('The bot has chosen the following move: ', bot_move)
    game_id = game.id
    with rlock(get_game_lock_redis_key(game_id)):
        game_json = rget_json(get_game_redis_key(game_id))
        game_from_json = Game.from_json(game_json)

        assert game_from_json.game_state

        if not game.game_state.has_moved_by_player[1 - player_num]:
            rset_json(get_game_with_hidden_information_redis_key(game.id), {1 - player_num: game.to_json()}, ex=24 * 60 * 60)

        try:
            for card_id, lane_number in bot_move.items():
                game_from_json.game_state.play_card(player_num, card_id, lane_number)
        except Exception:
            print(f'The bot tried to play an invalid move: {bot_move}.')
            hidden_info_game = rget_json(get_game_with_hidden_information_redis_key(game.id))
            if hidden_info_game is not None and hidden_info_game.get(player_num) is not None:
                game_from_hidden_json = Game.from_json(hidden_info_game[player_num])
                assert game_from_hidden_json.game_state
                bot_move = find_bot_move(player_num, game_from_hidden_json.game_state)
            else:
                game_from_nonhidden_json = Game.from_json(game_json)
                assert game_from_nonhidden_json.game_state
                bot_move = find_bot_move(player_num, game_from_nonhidden_json.game_state)

            try:
                for card_id, lane_number in bot_move.items():
                    game_from_json.game_state.play_card(player_num, card_id, lane_number)
            except Exception:
                print(f'The bot tried to play an invalid move: {bot_move} again. Giving up.')

        game_from_json.game_state.has_moved_by_player[player_num] = True        

        have_moved = game_from_json.game_state.all_players_have_moved()
        if have_moved:
            game_from_json.game_state.roll_turn()
            rdel(get_game_with_hidden_information_redis_key(game.id))

        rset_json(get_game_redis_key(game_id), game_from_json.to_json(), ex=24 * 60 * 60)

        if have_moved:
            socketio.emit('update', room=game_id)



def recurse_to_json(obj):
    if isinstance(obj, dict):
        return {k: recurse_to_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recurse_to_json(v) for v in obj]
    elif hasattr(obj, 'to_json'):
        return obj.to_json()
    else:
        return obj


# decorator that takes in an api endpoint and calls recurse_to_json on its result
def api_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try: 
            return func(*args, **kwargs)
        except Exception as e:
            print(traceback.print_exc())
            return jsonify({"error": "Unexpected error"}), 500

    return wrapper


@app.route('/api/card_pool', methods=['GET'])
@api_endpoint
def get_card_pool():
    print('Getting card pool')
    return recurse_to_json({'cards': CARD_TEMPLATES, 'laneRewards': LANE_REWARDS})


@app.route('/api/decks', methods=['POST'])
@api_endpoint
def create_deck():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    cards = data.get('cards')
    if not cards:
        return jsonify({"error": "Cards data is required"}), 400

    username = data.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    deck_name = data.get('name')
    if not deck_name:
        return jsonify({"error": "Deck name is required"}), 400

    lane_reward_name = data.get('laneRewardName') or None

    # Process the cards data as needed, e.g., save to a database or check game state
    with rlock('decks'):
        decks = rget_json('decks') or {}
        deck = Deck(cards, username, deck_name, associated_lane_reward_name=lane_reward_name)
        deck_id = deck.id
        decks[deck_id] = deck.to_json()
        rset_json('decks', decks)

    return jsonify(deck.to_json())


@app.route('/api/decks', methods=['GET'])
@api_endpoint
def get_decks():
    decks_json = rget_json('decks') or {}
    decks = [Deck.from_json(deck_json) for deck_json in decks_json.values()]
    return recurse_to_json([deck for deck in decks if deck.username in [request.args.get('username'), COMMON_DECK_USERNAME]])


@app.route('/api/host_game', methods=['POST'])
@api_endpoint
def host_game():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    deck_id = data.get('deckId')

    if not deck_id:
        return jsonify({"error": "Deck ID is required"}), 400
    
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    host_game_id = data.get('hostGameId')

    is_bot_game = bool(data.get('bot_game'))
    
    decks = rget_json('decks') or {}
    deck_json = decks.get(deck_id)
    if not deck_json:
        return jsonify({"error": "Deck not found"}), 404
    deck = Deck.from_json(deck_json)

    if is_bot_game:
        bot_deck = get_bot_deck(deck.name) or deck
        game = Game({0: username, 1: 'RUFUS_THE_ROBOT'}, {0: deck, 1: bot_deck}, id=host_game_id)
        game.is_bot_by_player[1] = True
        game.start()
        
        socketio.emit('update', room=game.id)      

        assert game.game_state
        bot_take_mulligan(game.game_state, 1)

        start_new_thread(bot_move_in_game, (game, 1))

    else:
        game = Game({0: username, 1: None}, {0: deck, 1: None}, id=host_game_id)

    with rlock(get_game_lock_redis_key(game.id)):
        rset_json(get_game_redis_key(game.id), game.to_json(), ex=24 * 60 * 60)

    return jsonify({"gameId": game.id})


@app.route('/api/join_game', methods=['POST'])
@api_endpoint
def join_game():
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    game_id = data.get('gameId')

    if not game_id:
        return jsonify({"error": "Game ID is required"}), 400
    
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    deck_id = data.get('deckId')

    if not deck_id:
        return jsonify({"error": "Deck ID is required"}), 400

    with rlock(get_game_lock_redis_key(game_id)):
        game_json = rget_json(get_game_redis_key(game_id))
        if not game_json:
            return jsonify({"error": "Game not found"}), 404
        
        game = Game.from_json(game_json)

        decks = rget_json('decks') or {}
        deck_json = decks.get(deck_id)
        if not deck_json:
            return jsonify({"error": "Deck not found"}), 404
        deck = Deck.from_json(deck_json)

        game.usernames_by_player[1] = username
        game.decks_by_player[1] = deck
        game.start()
        
        rset_json(get_game_redis_key(game.id), game.to_json(), ex=24 * 60 * 60)

        socketio.emit('update', room=game.id)
    
    return jsonify({"gameId": game.id})


@app.route('/api/games/<game_id>', methods=['GET'])
@api_endpoint
def get_game(game_id):
    player_num = int(raw_player_num) if (raw_player_num := request.args.get('playerNum')) is not None else None

    game_json = rget_json(get_game_redis_key(game_id))

    if not game_json:
        return jsonify({"error": "Game not found"}), 404   

    game = Game.from_json(game_json)

    first_turn = game.game_state is not None and game.game_state.turn == 1

    if player_num is not None and not first_turn and (hidden_game_info := rget_json(get_game_with_hidden_information_redis_key(game_id))) and hidden_game_info.get(player_num):
        # Intentionally give a slightly stale game if one exists to the opponent who might have refreshed their page
        print('Returning the things ')
        return jsonify(hidden_game_info[player_num])

    return recurse_to_json(game_json)


@app.route('/api/games/<game_id>/take_turn', methods=['POST'])
@api_endpoint
def take_turn(game_id):
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    cards_to_lanes = data.get('cardsToLanes')

    if cards_to_lanes is None:
        return jsonify({"error": "Cards mapping is required"}), 400
    
    with rlock(get_game_lock_redis_key(game_id)):
        game_json = rget_json(get_game_redis_key(game_id))
        if not game_json:
            return jsonify({"error": "Game not found"}), 404

        game = Game.from_json(game_json)

        player_num = game.username_to_player_num(username)
        assert player_num is not None
        assert game.game_state is not None

        if not game.game_state.has_moved_by_player[1 - player_num]:
            rset_json(get_game_with_hidden_information_redis_key(game.id), {1 - player_num: game.to_json()}, ex=24 * 60 * 60)

        for card_id, lane_number in cards_to_lanes.items():
            game.game_state.play_card(player_num, card_id, lane_number)

        game.game_state.has_moved_by_player[player_num] = True
        have_moved = game.game_state.all_players_have_moved()
        if have_moved:
            game.game_state.roll_turn()
            rdel(get_game_with_hidden_information_redis_key(game.id))

        if game.is_bot_by_player[1 - player_num] and not game.game_state.has_moved_by_player[1 - player_num]:
            start_new_thread(bot_move_in_game, (game, 1 - player_num))

        rset_json(get_game_redis_key(game.id), game.to_json(), ex=24 * 60 * 60)
    
    if have_moved:
        socketio.emit('update', room=game.id)

    return jsonify({"gameId": game.id,
                    "game": game.to_json()})

@app.route('/api/games/<game_id>/mulligan', methods=['POST'])
@api_endpoint
def mulligan(game_id):
    data = request.json

    if not data:
        return jsonify({"error": "Invalid data"}), 400
    
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    cards_to_mulligan = data.get('cards')

    if cards_to_mulligan is None:
        return jsonify({"error": "Cards mapping is required"}), 400
    
    with rlock(get_game_lock_redis_key(game_id)):
        game_json = rget_json(get_game_redis_key(game_id))
        if not game_json:
            return jsonify({"error": "Game not found"}), 404

        game = Game.from_json(game_json)

        player_num = game.username_to_player_num(username)
        assert player_num is not None
        assert game.game_state is not None

        random.shuffle(cards_to_mulligan)

        for card_id in cards_to_mulligan:
            game.game_state.mulligan_card(player_num, card_id)

        game.game_state.has_mulliganed_by_player[player_num] = True

        rset_json(get_game_redis_key(game.id), game.to_json(), ex=24 * 60 * 60)
    
    # Silly kludge to prevent leakage of hidden info because I didn't want to bother using the hidden_game_info logic
    for lane in game.game_state.lanes:
        lane.characters_by_player[0] = [character for character in lane.characters_by_player[0] if not character.template.name == 'Elephant Rat']
        lane.characters_by_player[1] = [character for character in lane.characters_by_player[1] if not character.template.name == 'Elephant Rat']

    return jsonify({"gameId": game.id,
                    "game": game.to_json()})


@socketio.on('connect')
def on_connect():
    print('Connected')

@socketio.on('join')
def on_join(data):
    username = data['username'] if 'username' in data else 'anonymous'
    room = data['room']
    join_room(room)
    print(f'{username} joined {room}')
    
@socketio.on('leave')
def on_leave(data):
    username = data['username'] if 'username' in data else 'anonymous'
    room = data['room']
    leave_room(room)
    print(f'{username} left {room}') 

if __name__ == '__main__':
    create_common_decks()

    if LOCAL:
        socketio.run(app, host='0.0.0.0', port=5001, debug=True)
    else:
        socketio.run(app, host='0.0.0.0', port=5007)
