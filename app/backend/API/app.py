from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import uuid

from sqlalchemy.orm import Session
from backend.database import deps

from backend.API.schemas import GameConfig, PlayerMove

from backend.database import crud, models
from backend.database.database import engine, Base

from backend.game_scripts import main

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/frontend/dist", StaticFiles(directory="frontend/dist"), name="frontend-dist")

@app.get("/")
def serve_home():
    return FileResponse("frontend/dist/index.html")

@app.get("/play")
def serve_play():
    return FileResponse("frontend/dist/play.html")

@app.get("/game")
def serve_play():
    return FileResponse("frontend/dist/game.html")

@app.post("/create-game")
def create_game(config: GameConfig, db: Session = Depends(deps.get_db)):
    game = main.create_game(config.difficulty, config.height, config.width, config.full)
    game_data = main.get_game_data(game)
    uuid = crud.create_game(db, game_data)
    return {"game_id": uuid}

@app.get("/{game_id}")
def get_game(game_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    game_data = crud.get_game(db, game_id)
    game_over = main.is_game_over(main.restore_game_from_data(game_data))
    return {"game": game_data, "game_over": game_over}

@app.put("/{game_id}/ai")
def start_game(game_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    game_data = crud.get_game(db, game_id)
    game = main.restore_game_from_data(game_data)
    val = main.make_ai_move(game)
    game_data = main.get_game_data(game)
    crud.update_game(db, game_id, game_data)
    return {"valid_move": val}

@app.put("/{game_id}/move")
def player_move(game_id: uuid.UUID, move: PlayerMove, db: Session = Depends(deps.get_db)):
    game_data = crud.get_game(db, game_id)
    game = main.restore_game_from_data(game_data)
    if not main.make_player_move(game, move.move):
        return {"valid_move": False}
    game_data = main.get_game_data(game)
    crud.update_game(db, game_id, game_data)
    return {"valid_move": True}