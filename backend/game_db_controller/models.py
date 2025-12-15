import uuid
import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image_link = Column(String)
    description = Column(String, nullable=False)
    studio = Column(String, nullable=False)
    available_copies = Column(Integer, nullable=False, default=0)

class GameCategoriesEnum(str, enum.Enum):
    Action = "Action"
    Puzzle = "Puzzle"
    Adventure = "Adventure"
    Strategy = "Strategy"
    RPG = "RPG"
    FPS = "FPS"
    Sports = "Sports"
    Racing = "Racing"

class GameCategory(Base):
    __tablename__ = "game_category"
    category = Column(Enum(GameCategoriesEnum), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), primary_key=True)
    
    game = relationship("Game", backref="game_categories")

class Comment(Base):
    __tablename__ = "comment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    contents = Column(Text, nullable=False)

    game = relationship("Game", backref="comments")
