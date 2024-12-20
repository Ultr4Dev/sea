from pydantic import BaseModel, Field


class Fish(BaseModel):
    name: str
    description: str
    id: str = Field(
        ...,
        pattern="^Fish-[a-zA-Z0-9]{16}$",
        exclude=False,
    )
    sea_id: str = Field(..., pattern="^Sea-[a-zA-Z0-9]{16}$")
    data: dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Nemo",
                    "description": "A small orange fish.",
                    "id": "Fish-1234567890abcdef",
                    "sea_id": "Sea-1234567890abcdef",
                    "data": {"color": "orange", "size": "small"},
                }
            ]
        }
    }


class FishCreate(BaseModel):
    name: str
    description: str
    data: dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Nemo",
                    "description": "A small orange fish.",
                    "data": {"color": "orange", "size": "small"},
                }
            ]
        }
    }
