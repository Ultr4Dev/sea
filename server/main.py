from os import environ
import fastapi
import database
from sqlalchemy.orm import Session
from fastapi import FastAPI

from routes.stats import stats
from routes.sea import sea
from admin import middleware as admin

app = FastAPI()
responses = {
    404: {"description": "The resource was not found."},
    500: {
        "description": "The server encountered an unexpected condition that prevented it from fulfilling the request.",
    },
}
db = database
db.Base.metadata.drop_all(db.engine)  # Drop all tables if they exist
db.Base.metadata.create_all(db.engine)  # Recreate tables
app.servers = [{"url": environ.get("COOLIFY_URL", "http://localhost:8000")}]
app.include_router(prefix="/V1", router=sea.router, tags=[], responses=responses)
app.include_router(stats.router, tags=[], responses=responses)
app.include_router(admin.router, responses=responses)
app.router.tags = []
app.title = "Plenty Of Fish In The Sea"
app.description = """
The Sea API is a free solution for storing and retrieving JSON data. It is designed to be simple and easy to use.

**I will not be responsible for any data loss or corruption as i do not actually care about your data. There is no backup system in place or security measures. Use at your own risk.**
"""


@app.get(
    "/",
    tags=["default"],
)
def read_root():
    return fastapi.responses.RedirectResponse("/redoc")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
