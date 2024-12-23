import logging
from app.v1.main import app

logging.basicConfig(level=logging.DEBUG)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8994)
