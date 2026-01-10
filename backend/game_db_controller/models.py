import uuid
import enum
from sqlalchemy.sql import func
from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base() #has to be global or nothing works

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

class PlatformType(str, enum.Enum):
    PS4 = "PS4"
    PS5 = "PS5"
    Xbox_One = "Xbox One"
    Xbox_SX = "Xbox SX"
    Switch = "Switch"
    Switch_2 = "Switch 2"

class GameCategory(Base):
    __tablename__ = "game_category"
    category = Column(Enum(GameCategoriesEnum), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), primary_key=True)
    
    game = relationship("Game", backref="game_categories")

class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    contents = Column(Text, nullable=False)

    game = relationship("Game", backref="comments")

class Copy(Base):
    __tablename__ = "copy"

    copy_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    lang_version = Column(Text, nullable=False)
    platform = Column( #unholy mess so it uses values and not names
    Enum(
        PlatformType,
        name="platform_type",
        values_callable=lambda enum_cls: [e.value for e in enum_cls] #e.names doesnt work
    ),
    nullable=False
    )
    available = Column(Boolean, nullable=False, default=True)

    game = relationship("Game", backref="copies")

class Borrow(Base):
    __tablename__ = "borrow"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    copy_id = Column(UUID(as_uuid=True), ForeignKey("copy.copy_id", ondelete="CASCADE"), primary_key=True)
    borrow_start_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    copy = relationship("Copy", backref="borrows")