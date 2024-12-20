import fastapi
import database
from routes.fish import models
from fastapi import APIRouter

"""
    Fish (data)
"""
router = APIRouter(tags=["fish"])
db = database


@router.post(
    "/{sea_id}/fish/",
    status_code=201,
    response_model=models.Fish,
)
def create_fish(sea_id: str, fish: models.FishCreate) -> models.Fish:
    sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()
    if not sea:
        raise fastapi.HTTPException(status_code=404)
    db_fish = db.Fish(
        data=fish.data,
        sea_id=sea_id,
        sea=sea,
        name=fish.name,
        description=fish.description,
    )
    db.session.add(db_fish)
    db.session.commit()
    # Check if sea exists
    sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()
    if not sea:
        raise fastapi.HTTPException(status_code=404)
    if not db_fish:
        # If fish is not created
        raise fastapi.HTTPException(status_code=404)

    return db_fish


@router.get("/{sea_id}/fish/")
def get_fishes(sea_id: str) -> list[models.Fish]:
    fish = db.session.query(db.Fish).filter(db.Fish.sea_id == sea_id).all()
    if not fish:
        raise fastapi.HTTPException(status_code=404)
    return fish


@router.get("/{sea_id}/fish/{fish_id}")
def get_fish(sea_id: str, fish_id: str) -> models.Fish:
    fish = (
        db.session.query(db.Fish)
        .filter(db.Fish.id == fish_id, db.Fish.sea_id == sea_id)
        .first()
    )
    if not fish:
        raise fastapi.HTTPException(status_code=404)
    return fish


@router.delete("/{sea_id}/fish/{fish_id}")
def delete_fish(sea_id: str, fish_id: str):
    db.session.query(db.Fish).filter(
        db.Fish.id == fish_id, db.Fish.sea_id == sea_id
    ).delete()
    db.session.commit()

    return {"message": "Fish deleted."}
