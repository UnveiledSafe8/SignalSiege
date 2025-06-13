from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import uuid
import json

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
    uuid = crud.create_game(db, config)
    return {"game_id": uuid}