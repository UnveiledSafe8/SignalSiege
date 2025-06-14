from sqlalchemy.orm import Session
from . import models
from backend.API import schemas

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