from pydantic import BaseModel

class GameConfig(BaseModel):
    height: int
    width: int
    full: bool
    opponent: str
    difficulty: str

class GameState(BaseModel):
    game_state: str

class PlayerMove(BaseModel):
    move: str