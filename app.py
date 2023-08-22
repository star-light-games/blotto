from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Dummy data to simulate the backend database or game state
CARDS = [
    {"id": 1, "name": "Card 1"},
    {"id": 2, "name": "Card 2"},
    {"id": 3, "name": "Card 3"},
    {"id": 4, "name": "Card 4"},
]

@app.route('/api/hand', methods=['GET'])
def get_hand():
    # In a real scenario, you might want to select cards dynamically
    return jsonify(CARDS)

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