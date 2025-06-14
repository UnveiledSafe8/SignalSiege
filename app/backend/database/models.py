from sqlalchemy import ForeignKey, Column, BigInteger, Enum, Integer, CheckConstraint, String, Float
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
import uuid
import enum

class StateEnum(enum.Enum):
    completed = "COMPLETED"
    zombie = "ZOMBIE"
    inprogress = "INPROGRESS"
    initiated = "INITIATED"

class DifficultyEnum(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    very_hard = "very_hard"
    insane = "insane"
    self = "self"

class Game(Base):
    __tablename__ = "games_info"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, nullable=False)
    turns = Column(JSONB, nullable=False)
    players = Column(JSONB, nullable=False)
    ai_player_colors = Column(ARRAY(String), nullable=True)
    difficulty = Column(Enum(DifficultyEnum), nullable=False)
    komi = Column(Float, nullable=False)
    graph = Column(JSONB, nullable=False)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    passes = Column(Integer, nullable=False)

    game_status = relationship("Status", back_populates="game_info")

    __table_args__ = (
        CheckConstraint('height >= 3 AND height <= 20', name='check_height_range'),
        CheckConstraint('width >= 3 AND width <= 20', name='check_width_range'),
    )

class Status(Base):
    __tablename__ = "games_status"
    id = Column(BigInteger, primary_key=True, nullable=False)
    state = Column(Enum(StateEnum), nullable=False)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games_info.id"))

    game_info = relationship("Game", back_populates="game_status")