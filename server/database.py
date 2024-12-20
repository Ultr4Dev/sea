from typing import Dict, List
from typing import Optional
from sqlalchemy import JSON, ForeignKey, create_engine
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from utils import random_string


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

    __tablename__ = "sea"

    id = mapped_column(String, primary_key=True, default=f"Sea-{random_string(16)}")
    name = mapped_column(String)
    description = mapped_column(String)
    fish = relationship("Fish", back_populates="sea")


class Fish(Base):
    """
    Represents a fish entity in the database.

    Attributes:
        name (str): The name of the fish.
        description (str): A description of the fish.
        data (str): JSON data.
        sea_id (str): The identifier of the sea where the fish lives.
        sea (Sea): The sea where the fish lives.
    """

    __tablename__ = "fish"

    id = mapped_column(String, primary_key=True, default=f"Fish-{random_string(16)}")
    name = mapped_column(String)
    description = mapped_column(String)
    data = mapped_column(JSON(True))
    sea_id = mapped_column(String, ForeignKey("sea.id"))
    sea = relationship("Sea", back_populates="fish")


# Stats


engine = create_engine("sqlite:///db.db", echo=True)
Base.metadata.create_all(engine, tables=[Sea.__table__, Fish.__table__])
session = Session(engine)
