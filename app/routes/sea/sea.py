import fastapi
import app.database as database
from app.routes.sea import models
from fastapi import APIRouter

from app.routes.fish import fish

"""
    Sea (location of fish(data))
"""

router = APIRouter(prefix="/sea")
router.include_router(fish.router, tags=["fish"])
db = database


@router.post(f"/", status_code=201, tags=["sea"])
def create_sea(sea: models.SeaCreate) -> models.Sea:
    db_sea = db.Sea(name=sea.name, description=sea.description)
    db.session.add(db_sea)
    db.session.commit()

    return db_sea


@router.get("/{sea_id}", tags=["sea"])
def get_sea(sea_id: str) -> models.Sea:
    sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()
    if not sea:
        raise fastapi.HTTPException(status_code=404)
    # Check if sea has fish

    return sea


@router.delete("/{sea_id}", tags=["sea"])
def delete_sea(sea_id: str) -> models.Sea:
    sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()
    if not sea:
        raise fastapi.HTTPException(status_code=404)
    db.session.delete(sea)
    db.session.commit()
    return sea
