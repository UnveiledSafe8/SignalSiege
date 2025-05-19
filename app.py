from flask import Flask, request, jsonify, send_from_directory
from backend.scripts_py.main import create_game, get_game, make_player_move, make_ai_move, is_game_over

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/start", methods=["POST"])
def start_game():
    data = request.json
    game_id = data["game_id"]
    difficulty = data["difficulty"]
    height = data["height"]
    width = data["width"]
    full = data.get("full", True)

    game = create_game(game_id, difficulty, height, width, full)
    return jsonify({
        "message": "Game started",
        "state": str(game),
        "turn": game.get_player_turn().color
    })

@app.route("/move/<game_id>", methods=["POST"])
def player_move(game_id):
    game = get_game(game_id)

    if not game:
        return jsonify({"error": "Game not found"}), 404

    move = request.json.get("move")
    if not move:
        return jsonify({"error": "No move provided"}), 400

    if game.is_Ai_turn():
        return jsonify({"error": "It's the AI's turn"}), 400

    if not make_player_move(game, move):
        return jsonify({"error": "Invalid move"}), 400

    make_ai_move(game)

    return jsonify({
        "message": "Move processed",
        "state": str(game),
        "turn": game.get_player_turn().color,
        "game_over": is_game_over(game)
    })

@app.route("/state/<game_id>", methods=["GET"])
def get_state(game_id):
    game = get_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    return jsonify({
        "state": str(game),
        "turn": game.get_player_turn().color,
        "game_over": is_game_over(game)
    })