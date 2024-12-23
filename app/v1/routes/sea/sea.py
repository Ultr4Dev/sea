import fastapi
from app.v1 import utils
import app.v1.database as database
from app.v1.routes.sea import models
from fastapi import APIRouter

from app.v1.routes.fish import fish

"""
    Sea (location of fish(data))
"""

router = APIRouter(prefix="/sea")
router.include_router(fish.router, tags=["v1"])
db = database


@router.post(f"/", status_code=201, tags=["v1"])
def create_sea(sea: models.SeaCreate) -> models.Sea:
    db_sea = db.Sea(name=sea.name, description=sea.description)
    db.session.add(db_sea)
    db.session.commit()

    return db_sea


@router.get("/{sea_id}", tags=["v1"])
def get_sea(sea_id: str) -> models.Sea:

    sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()
    if not sea:
        raise fastapi.HTTPException(status_code=404, detail="Sea not found.")
    # Check if sea has fish

    return sea


@router.delete("/{sea_id}", tags=["v1"])
def delete_sea(sea_id: str) -> models.Sea:

    sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()
    if not sea:
        raise fastapi.HTTPException(status_code=404)
    db.session.delete(sea)
    db.session.commit()
    return fastapi.responses.JSONResponse(
        content={"detail": "Sea deleted successfully."}
    )
