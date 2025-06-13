from sqlalchemy.orm import Session
from . import models
from backend.API import schemas

def create_game(db: Session, config: schemas.GameConfig, game):
    new_game = models.Game(height=config.height, width=config.width, full=config.full, difficulty=config.difficulty, game=game)
    db.add(new_game)
    db.add(models.Status(state=models.StateEnum.initiated, game_id=new_game.id))
    db.commit()
    return new_game.id