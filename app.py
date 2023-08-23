from card_templates_list import CARD_TEMPLATES
from deck import Deck
from flask import Flask, jsonify, request
from flask_cors import CORS
from game import Game

from redis_utils import rget, rget_json, rlock, rset_json
from utils import generate_unique_id

app = Flask(__name__)
CORS(app)


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
    def wrapper(*args, **kwargs):
        return jsonify(recurse_to_json(func(*args, **kwargs)))
    return wrapper


@app.route('/api/card_pool', methods=['GET'])
@api_endpoint
def get_card_pool():
    return recurse_to_json(CARD_TEMPLATES)


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

    # Process the cards data as needed, e.g., save to a database or check game state
    with rlock('decks'):
        decks = rget_json('decks') or {}
        deck = Deck(cards, username, deck_name)
        deck_id = deck.id
        rset_json('decks', decks)

    return jsonify({"deckId": deck_id})


@app.route('/api/decks', methods=['GET'])
@api_endpoint
def get_decks():
    decks = rget_json('decks') or {}
    return [deck for deck in list(decks.values()) if deck.username == request.args.get('username')]


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
    
    with rlock('games'):
        decks = rget_json('decks') or {}
        deck = decks.get(deck_id)
        if not deck:
            return jsonify({"error": "Deck not found"}), 404

        game = Game({0: username, 1: None}, {0: deck, 1: None})
        games = rget_json('games') or {}
        games[game.id] = game
        rset_json('games', games)
    
    return jsonify({"gameId": game.id})


@app.route('/api/games', methods=['GET'])
@api_endpoint
def get_games():
    games = rget_json('games') or {}
    return list(games.values())


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

    with rlock('games'):
        games = rget_json('games') or {}
        game = games.get(game_id)
        if not game:
            return jsonify({"error": "Game not found"}), 404

        game.usernames_by_player[1] = username
        game.deck_by_player[1] = deck_id
        game.start()
        rset_json('games', games)
    
    return jsonify({"gameId": game.id})


@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    lanes = data.get('lanes')
    if not lanes:
        return jsonify({"error": "Lanes data is required"}), 400

    # Process the lanes data as needed, e.g., save to a database or check game state
    print("Received lanes data:", lanes)

    return jsonify({"message": "Data received successfully"})

if __name__ == '__main__':
    app.run(debug=True)