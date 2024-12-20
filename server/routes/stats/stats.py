import fastapi
import database
from fastapi import APIRouter

"""
    Stats
"""
router = APIRouter(tags=["stats"])
db = database


@router.get("/stats")
def get_stats() -> dict:
    return {
        "total_seas": db.session.query(db.Sea).count(),
        "total_fish": db.session.query(db.Fish).count(),
    }
