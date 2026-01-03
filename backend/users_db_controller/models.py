import uuid
from sqlalchemy import Column, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base() #has to be global or nothing works

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(CITEXT, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    provider = Column(String, nullable=False, default="local")
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(Text)
    verification_token_expires = Column(DateTime)
    pending_email = Column(CITEXT)
    email_change_token = Column(Text)
    email_change_token_expires = Column(DateTime)
    password_reset_token = Column(Text)
    password_reset_token_expires = Column(DateTime)
    is_deletion_pending = Column(Boolean, nullable=False, default=False)
    deletion_scheduled_at = Column(DateTime)

    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class UserRole(Base):
    __tablename__ = "user_role"

    role = Column(String, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="roles")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    token = Column(Text, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="refresh_tokens")
