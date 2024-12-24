import http
import fastapi
import sqlalchemy
import sqlalchemy.orm
import app.v1.database as database
from app.v1.routes.fish import models
from fastapi import APIRouter, HTTPException, logger

"""
    Fish (data)
"""
router = APIRouter(tags=["v1"])
db = database


@router.post(
    "/{sea_id}/fish/",
    status_code=201,
    response_model=models.Fish,
)
def create_fish(sea_id: str, fish: models.FishCreate) -> models.Fish:
    try:
        sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()

        db_fish = db.Fish(
            data=fish.data,
            sea_id=sea_id,
            sea=sea,
            name=fish.name,
            description=fish.description,
        )
        db.session.add(db_fish)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        # Rollback the transaction
        db.session.rollback()

        if "NOT NULL constraint failed" in str(e):
            raise HTTPException(
                status_code=http.HTTPStatus.CONFLICT,
                detail="Could not create fish. Most likely the sea does not exist.",
            )
        else:
            raise e

    return db_fish


@router.get("/{sea_id}/fish/")
def get_fishes(sea_id: str) -> list[models.Fish]:
    fish = db.session.query(db.Fish).filter(db.Fish.sea_id == sea_id).all()
    if not fish:
        raise fastapi.HTTPException(status_code=404, detail="Sea has no fish.")
    return fish


@router.get("/{sea_id}/fish/{fish_id}")
def get_fish(sea_id: str, fish_id: str) -> models.Fish:
    fish = (
        db.session.query(db.Fish)
        .filter(db.Fish.id == fish_id, db.Fish.sea_id == sea_id)
        .first()
    )
    if not fish:
        raise fastapi.HTTPException(status_code=404, detail="Fish not found.")
    return fish


@router.delete("/{sea_id}/fish/{fish_id}")
def delete_fish(sea_id: str, fish_id: str):
    db.session.query(db.Fish).filter(
        db.Fish.id == fish_id, db.Fish.sea_id == sea_id
    ).delete()
    db.session.commit()

    return fastapi.responses.JSONResponse(
        content={"detail": "Fish deleted successfully."}
    )
