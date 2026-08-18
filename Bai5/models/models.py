from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False,
        default="user"
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    resources = relationship(
        "Resource",
        back_populates="owner",
        cascade="all, delete"
    )


class Resource(Base):
    __tablename__ = "resources"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(150),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    owner = relationship(
        "User",
        back_populates="resources"
    )