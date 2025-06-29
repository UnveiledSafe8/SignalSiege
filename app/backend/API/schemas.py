from pydantic import BaseModel, Field
from typing import Literal, Annotated

class GameConfig(BaseModel):
    height: Annotated[int, Field(ge=3, le=20)]
    width: Annotated[int, Field(ge=3, le=20)]
    full: bool
    difficulty: Literal["easy", "medium", "hard", "very_hard", "insane", "self"]

class PlayerMove(BaseModel):
    move: str = Field(pattern='^(\d+\.\d+|pass)$')

class User(BaseModel):
    email: str
    password: str