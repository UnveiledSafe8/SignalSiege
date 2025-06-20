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

    game_status = relationship("Status", back_populates="game_info", uselist=False)

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




class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True, unique=True, default=None)
    hashed_password = Column(String, nullable=False)

    settings = relationship("UserSettings", back_populates="user", uselist=False)
    stats = relationship("UserStats", back_populates="user", uselist=False)

class UserSettings(Base):
    __tablename__ = "settings"

    id = Column(BigInteger, primary_key=True, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="settings")

class UserStats(Base):
    __tablename__ = "user_statistics"

    id = Column(BigInteger, primary_key=True, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)    
    user = relationship("User", back_populates="stats")

    ai_stats = relationship("AiStats", back_populates="user_stats")

class AiStats(Base):
    __tablename__ = "ai_statistics"
    
    id = Column(BigInteger, primary_key=True)
    difficulty = Column(Enum(DifficultyEnum), nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    min_turns = Column(Integer, default=0)
    max_turns = Column(Integer, default=0)
    total_points_scored = Column(Float, default=0)

    user_stats_id = Column(BigInteger, ForeignKey("user_statistics.id"), nullable=False)
    user_stats = relationship("UserStats", back_populates="ai_stats")