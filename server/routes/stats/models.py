from calendar import c
from tkinter import N
from uuid import uuid4
from pydantic import UUID4, BaseModel, Field

from utils import random_string


class Stats(BaseModel):
    total_fish: int
    total_seas: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_fish": 100,
                    "total_seas": 10,
                }
            ]
        }
    }
