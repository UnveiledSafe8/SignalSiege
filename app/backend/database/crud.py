from sqlalchemy.orm import Session
from . import models

import json, uuid

def create_game(db: Session, game: dict):
    new_game = models.Game(turns=json.dumps(game["turns"]), players=json.dumps(game["players"]),ai_player_colors=game["ai_players"], difficulty=game["difficulty"],
                           komi=game["komi"], graph=json.dumps(game["graph"]), height=game["height"], width=game["width"], passes=game["passes"])
    db.add(new_game)
    db.add(models.Status(state=models.StateEnum.initiated, game_id=new_game.id))
    db.commit()
    return new_game.id

def get_game(db: Session, id: uuid.UUID):
    game = db.query(models.Game).filter(models.Game.id == id).first()
    game = {
        "turns": json.loads(game.turns),
        "players": json.loads(game.players),
        "ai_players": game.ai_player_colors,
        "difficulty": game.difficulty,
        "komi": game.komi,
        "graph": json.loads(game.graph),
        "height": game.height,
        "width": game.width,
        "passes": game.passes
    }
    return game

def update_game(db: Session, id: uuid.UUID, game_data: dict):
    game = db.query(models.Game).filter(models.Game.id == id).first()
    game.turns = json.dumps(game_data["turns"])
    game.players = json.dumps(game_data["players"])
    game.graph = json.dumps(game_data["graph"])
    game.passes = game_data["passes"]
    db.commit()
    return

def create_user(db: Session, user_email: str, user_hashed_password):
    user = models.User(email=user_email, hashed_password=user_hashed_password)
    db.add(user)
    db.flush()

    user_settings = models.UserSettings(user_id=user.id)
    user_stats = models.UserStats(user_id=user.id)
    db.add_all([user_settings, user_stats])
    db.flush()

    difficulties = [d for d in models.DifficultyEnum]
    for diff in difficulties:
        ai_stat = models.AiStats(difficulty=diff, user_stats_id=user.id)
        user.stats.ai_stats.append(ai_stat)

    db.commit()
    return user.id

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_stats(user: models.User):
    if (not user):
        return {}

    return {ai_db.difficulty: {"difficulty": ai_db.difficulty, "wins": ai_db.wins, "losses": ai_db.losses, "min_turns": ai_db.min_turns, "max_turns": ai_db.max_turns} for ai_db in user.stats.ai_stats}

def get_user_info(user: models.User):
    if not user:
        return {}
    
    return {
        "email": user.email,
        "username": user.username
    }