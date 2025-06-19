from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

import uuid

from jose import jwt

from sqlalchemy.orm import Session
from backend.database import deps

from backend.API.schemas import GameConfig, PlayerMove, User

from backend.database import crud, models
from backend.database.database import engine, Base

from backend.game_scripts import main

from . import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/frontend/dist", StaticFiles(directory="frontend/dist"), name="frontend-dist")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login-user")

@app.get("/")
def serve_home():
    return FileResponse("frontend/dist/index.html")

@app.get("/play")
def serve_play():
    return FileResponse("frontend/dist/play.html")

@app.get("/game")
def serve_play():
    return FileResponse("frontend/dist/game.html")

@app.get("/login")
def serve_login():
    return FileResponse("frontend/dist/login.html")

@app.get("/register")
def server_register():
    return FileResponse("frontend/dist/register.html")

@app.get("/stats")
def server_register():
    return FileResponse("frontend/dist/stats.html")

@app.post("/create-game")
def create_game(config: GameConfig, db: Session = Depends(deps.get_db)):
    game = main.create_game(config.difficulty, config.height, config.width, config.full)
    game_data = main.get_game_data(game)
    uuid = crud.create_game(db, game_data)
    return {"game_id": uuid}

@app.get("/get-game/{game_id}")
def get_game(game_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    game_data = crud.get_game(db, game_id)
    game_over = main.is_game_over(main.restore_game_from_data(game_data))
    return {"game": game_data, "game_over": game_over}

@app.put("/ai/{game_id}")
def start_game(game_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    game_data = crud.get_game(db, game_id)
    game = main.restore_game_from_data(game_data)
    val = main.make_ai_move(game)
    game_data = main.get_game_data(game)
    crud.update_game(db, game_id, game_data)
    return {"valid_move": val}

@app.put("/move/{game_id}")
def player_move(game_id: uuid.UUID, move: PlayerMove, db: Session = Depends(deps.get_db)):
    game_data = crud.get_game(db, game_id)
    game = main.restore_game_from_data(game_data)
    if not main.make_player_move(game, move.move):
        return {"valid_move": False}
    game_data = main.get_game_data(game)
    crud.update_game(db, game_id, game_data)
    return {"valid_move": True}

@app.post("/register-user")
async def read_items(user: User, db: Session = Depends(deps.get_db)):
    existing_user = crud.get_user(db, user.email)
    if existing_user:
        return {"id": None}
    
    hashed_pw = auth.get_hashed_password(user.password)
    user_id = crud.create_user(db, user.email, hashed_pw)

    return {"id": user_id}

@app.post("/login-user")
def login(user_login: User, db: Session = Depends(deps.get_db)):
    user = crud.get_user(db, user_login.email)
    if not user or not auth.verify_password(user_login.password, user.hashed_password):
        return {"access_token": None, "token_type": "bearer"}
    
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/get-player-stats")
def get_stats(token: str = Depends(oauth2_scheme), db: Session = Depends(deps.get_db)):
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    user_email = payload.get("sub")

    user = crud.get_user(db, user_email)
    stats = crud.get_user_stats(db, user)

    return {"stats": stats}