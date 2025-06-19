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

    user_stats = models.UserStats(user_id=user.id)
    db.add(user_stats)
    db.flush()

    user_stats.easy_ai_stats = models.EasyAiStats()
    user_stats.medium_ai_stats = models.MediumAiStats()
    user_stats.hard_ai_stats = models.HardAiStats()
    user_stats.very_hard_ai_stats = models.VeryHardAiStats()
    user_stats.insane_ai_stats = models.InsaneAiStats()
    db.add_all([user_stats.easy_ai_stats, user_stats.medium_ai_stats, user_stats.hard_ai_stats,
                user_stats.very_hard_ai_stats, user_stats.insane_ai_stats])

    db.commit()
    return user.id

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_stats(db: Session, user: models.User):
    if not user:
        return {}
    
    return {
        "easy_ai_wins": user.stats.easy_ai_stats.wins,
        "easy_ai_losses": user.stats.easy_ai_stats.losses,
        "medium_ai_wins": user.stats.medium_ai_stats.wins,
        "medium_ai_losses": user.stats.medium_ai_stats.losses,
        "hard_ai_wins": user.stats.hard_ai_stats.wins,
        "hard_ai_losses": user.stats.hard_ai_stats.losses,
        "very_hard_ai_wins": user.stats.very_hard_ai_stats.wins,
        "very_hard_ai_losses": user.stats.very_hard_ai_stats.losses,
        "insane_ai_wins": user.stats.insane_ai_stats.wins,
        "insane_ai_losses": user.stats.insane_ai_stats.losses,
    }