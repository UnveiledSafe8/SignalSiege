from fastapi import FastAPI, Depends, Response, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

import uuid

from jose import jwt

from sqlalchemy.orm import Session
from backend.database import deps

from backend.API.schemas import GameConfig, PlayerMove, User

from backend.database import crud, models
from backend.database.database import engine, Base

from backend.game_scripts import main

from . import auth

import os

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
def serve_register():
    return FileResponse("frontend/dist/register.html")

@app.get("/stats")
def serve_stats():
    return FileResponse("frontend/dist/stats.html")

@app.get("/settings")
def serve_settings():
    return FileResponse("frontend/dist/settings.html")

@app.post("/create-game")
def create_game(config: GameConfig, db: Session = Depends(deps.get_db)):
    game = main.create_game(config.difficulty, config.height, config.width, config.full)
    game_data = main.get_game_data(game)
    uuid = crud.create_game(db, game_data)
    crud.update_game_state(db, uuid, "INITIATED")

    return {"game_id": uuid}

@app.get("/get-game/{game_id}")
def get_game(game_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    game_data = crud.get_game(db, game_id)
    game_over = main.is_game_over(main.restore_game_from_data(game_data))
    if game_over:
        crud.update_game_state(db, game_id, "COMPLETED")

    return {"game": game_data, "game_over": game_over}

@app.put("/ai/{game_id}")
def start_game(game_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    if crud.get_game_state(db, game_id) == "COMPLETED":
        return {"valid_move": False}
    
    game_data = crud.get_game(db, game_id)
    game = main.restore_game_from_data(game_data)
    val = main.make_ai_move(game)
    game_data = main.get_game_data(game)
    crud.update_game(db, game_id, game_data)
    crud.update_game_state(db, game_id, "ZOMBIE")
    return {"valid_move": val}

@app.put("/move/{game_id}")
def player_move(game_id: uuid.UUID, move: PlayerMove, db: Session = Depends(deps.get_db)):
    if crud.get_game_state(db, game_id) == "COMPLETED":
        return {"valid_move": False}
    
    game_data = crud.get_game(db, game_id)
    game = main.restore_game_from_data(game_data)
    if not main.make_player_move(game, move.move):
        return {"valid_move": False}
    game_data = main.get_game_data(game)
    crud.update_game(db, game_id, game_data)
    crud.update_game_state(db, game_id, "INPROGRESS")
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
def login(user_login: User, response: Response, db: Session = Depends(deps.get_db)):
    user = crud.get_user(db, user_login.email)
    if not user or not auth.verify_password(user_login.password, user.hashed_password):
        return {"login": False}
    
    token = auth.create_access_token({"sub": user.email})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=os.getenv("SECURE_HTTP"),
        samesite="Lax"
    )

    return {"login": True}

@app.get("/get-player-stats")
def get_stats(request: Request, db: Session = Depends(deps.get_db)):
    token = request.cookies.get("access_token")
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    user_email = payload.get("sub")

    user = crud.get_user(db, user_email)
    stats = crud.get_user_stats(user)

    return stats

@app.get("/get-player-info")
def get_info(request: Request, db: Session = Depends(deps.get_db)):
    token = request.cookies.get("access_token")
    payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
    user_email = payload.get("sub")

    user = crud.get_user(db, user_email)
    info = crud.get_user_info(user)

    return info

@app.get("/auth-me")
def is_auth(request: Request):
    token = request.cookies.get("access_token")

    if token:
        return {"login": True}
    else:
        return {"login": False}
    
@app.post("/logout-user")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"logout": True}