from pydantic import BaseModel, Field


class Sea(BaseModel):
    name: str
    description: str
    id: str = Field(
        ...,
        pattern="^Sea-[a-zA-Z0-9]{16}$",
        exclude=False,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Pacific Ocean",
                    "description": "The largest ocean on Earth.",
                    "id": "Sea-1234567890abcdef",
                }
            ]
        }
    }


class SeaCreate(BaseModel):
    name: str
    description: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Pacific Ocean",
                    "description": "The largest ocean on Earth.",
                }
            ]
        }
    }
