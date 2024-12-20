from pydantic import BaseModel


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
