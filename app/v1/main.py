from os import environ
import fastapi
from app.v1 import utils
import app.v1.database as database
from fastapi import FastAPI, HTTPException

from app.v1.routes.stats import stats
from app.v1.routes.sea import sea
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

db = database
db.Base.metadata.drop_all(db.engine)  # Drop all tables if they exist
db.Base.metadata.create_all(db.engine)  # Recreate tables
app.servers = [{"url": environ.get("COOLIFY_URL", "http://localhost:8994")}]
app.include_router(prefix="/v1", router=sea.router, tags=["v1"])
app.include_router(stats.router, tags=[])
# app.include_router(admin.router, responses=responses)
app.router.tags = []
app.title = "Plenty Of Fish In The Sea"
app.description = """
The Sea API is a free solution for storing and retrieving JSON data. It is designed to be simple and easy to use.

**I will not be responsible for any data loss or corruption as i do not actually care about your data. There is no backup system in place or security measures. Use at your own risk.**
"""
exceptionhandler = utils.ExceptionHandler()
# statuscheck = utils.StatusCheckMiddleware(app=exceptionhandler)


# app.add_middleware(BaseHTTPMiddleware, statuscheck)


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    exception = exceptionhandler.exception_handler(exc)
    return exception


@app.get("/", tags=["default"], include_in_schema=False)
def read_root() -> fastapi.responses.RedirectResponse:
    return fastapi.responses.RedirectResponse("/docs")


@app.get("/health", tags=["default"])
def health():
    if exceptionhandler.operational:
        return fastapi.responses.JSONResponse(status_code=200, content={"status": "ok"})
    return fastapi.Response(status_code=503)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8994)
