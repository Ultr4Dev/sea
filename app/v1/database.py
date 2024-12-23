import os
from sqlalchemy import JSON, ForeignKey, create_engine, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Session
from app.v1.utils import random_string


class Base(DeclarativeBase):
    pass


class Sea(Base):
    """
    Represents a sea entity in the database.

    Attributes:
        id (str): The unique identifier of the sea.
        name (str): The name of the sea.
        description (str): A description of the sea.
        fish (List[Fish]): A list of fish that live in the sea.
    """

    __tablename__ = "sea_v1"

    # Use default=lambda: to generate a new ID at runtime
    id = mapped_column(
        String,
        primary_key=True,
        default=lambda: random_string(16, "Sea-"),
    )
    name = mapped_column(String)
    description = mapped_column(String)
    fish = relationship("Fish", back_populates="sea_v1")


class Fish(Base):
    """
    Represents a fish entity in the database.

    Attributes:
        id (str): The unique identifier of the fish.
        name (str): The name of the fish.
        description (str): A description of the fish.
        data (dict): JSON data.
        sea_id (str): The identifier of the sea where the fish lives.
        sea (Sea): The sea where the fish lives.
    """

    __tablename__ = "fish_v1"

    id = mapped_column(
        String,
        primary_key=True,
        default=lambda: random_string(16, "Fish-"),
    )
    name = mapped_column(String)
    description = mapped_column(String)
    data = mapped_column(JSON)
    sea_id = mapped_column(String, ForeignKey("sea_v1.id"))
    sea = relationship("Sea", back_populates="fish_v1")


# Stats
engine = create_engine(os.environ.get("DATABASE_URL", "sqlite:///db.db"), echo=True)
Base.metadata.create_all(engine, tables=[Sea.__table__, Fish.__table__])
session = Session(engine)
