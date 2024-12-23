import time

import fastapi
import app.v1.database as database
from fastapi import APIRouter, FastAPI, Request

db = database


router = APIRouter(
    include_in_schema=False,
)


@router.get("/admin/stats")
def get_stats():
    return {
        "total_seas": db.session.query(db.Sea).count(),
        "total_fish": db.session.query(db.Fish).count(),
    }


@router.get("/admin/seas")
def get_seas():
    seas = db.session.query(db.Sea).all()
    return seas


@router.get("/admin/seas/stats")
def get_seas_stats():
    # Get all seas
    seas = db.session.query(db.Sea).all()
    # Get all fish
    fish = db.session.query(db.Fish).all()
    # Get all fish count
    fish_count = db.session.query(db.Fish).count()
    # Get all seas count
    seas_count = db.session.query(db.Sea).count()
    # Get all fish per sea
    fish_per_sea = {}
    for sea in seas:
        fish_per_sea[sea.id] = (
            db.session.query(db.Fish).filter(db.Fish.sea_id == sea.id).count()
        )

    # collect data
    data = {
        "total_seas": seas_count,
        "total_fish": fish_count,
        "fish_per_sea": fish_per_sea,
    }
    return data


@router.get("/admin/seas/{sea_id}")
def get_sea(sea_id: str):
    sea = db.session.query(db.Sea).filter(db.Sea.id == sea_id).first()
    if not sea:
        raise fastapi.HTTPException(status_code=404)
    sea_stats = db.session.query(db.Fish).filter(db.Fish.sea_id == sea_id).count()
    if not sea_stats:
        sea_stats = 0
    return {"sea": sea, "fish": sea_stats}


@router.get("/admin/seas/{sea_id}/fish")
def get_fish(sea_id: str):
    fish = (
        db.session.query(db.Fish).filter(db.Fish.sea_id == sea_id).with_labels().all()
    )
    return fish
