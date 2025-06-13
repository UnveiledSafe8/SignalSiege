from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.API.schemas import GameConfig, PlayerMove, GameState

from backend.game_scripts import main

app = FastAPI()

app.mount("/frontend/dist", StaticFiles(directory="frontend/dist"), name="frontend-dist")

games = []

@app.get("/")
def serve_home():
    return FileResponse("frontend/dist/index.html")

@app.get("/play")
def serve_play():
    return FileResponse("frontend/dist/play.html")

@app.get("/game")
def serve_play():
    return FileResponse("frontend/dist/game.html")

@app.get("/init")
def init_game():
    #database added later for processing ids
    return {"game_id": 0}

@app.post("/{game_id}/create")
async def create_game(game_id: int, config: GameConfig):
    if config.opponent == "local":
        config.difficulty = "self"
    game = main.create_game(config.difficulty, config.height, config.width, config.full)
    games.append(game)
    board, scores, difficulty, human_players, ai_players = main.get_game_summary(game)
    return {"board": board, "scores": scores, "difficulty": difficulty, "human_players": human_players, "ai_players": ai_players}

@app.get("/{game_id}/start")
async def start_game(game_id, background_tasks: BackgroundTasks):
    game = games[int(game_id)]
    background_tasks.add_task(main.make_ai_move, game)
    return {"game_start": True}

@app.put("/{game_id}/move")
async def player_move(game_id: int, move: PlayerMove, background_tasks: BackgroundTasks):
    game = games[0]
    valid_move = main.make_player_move(game, move.move) and not main.is_game_over(game)
    if valid_move:
        background_tasks.add_task(main.make_ai_move, game)
    board, scores, difficulty, human_players, ai_players = main.get_game_summary(game)
    return {"valid_move": valid_move, "board": board, "scores": scores, "difficulty": difficulty, "human_players": human_players, "ai_players": ai_players}

@app.get("/{game_id}/state")
def get_game_state(game_id: int):
    game = games[0]
    board, scores, difficulty, human_players, ai_players = main.get_game_summary(game)
    return {"board": board, "scores": scores, "difficulty": difficulty, "human_players": human_players, "ai_players": ai_players}