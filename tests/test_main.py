import logging
import fastapi
from pydantic import BaseModel
import pytest
from fastapi.testclient import TestClient

from app.v1.main import app
from app.v1.routes.fish import models as fish_models
from app.v1.routes.sea import models as sea_models

client = TestClient(app)


class world(BaseModel):

    name: str = "Pacific Ocean"
    description: str = "The largest ocean on Earth."
    sea_id: str = None
    fish_id: str = None


test_data = world()


def test_default_redirect():
    response = client.get("/")
    logging.info(response)
    assert response.status_code == 200
    assert response.url.path == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_sea_returns_404():
    """
    Test that the API returns 404 when the sea does not exist
    """
    response = client.get("/v1/sea/Sea-123")
    assert response.status_code == 404


def test_create_sea():
    """
    Test that the API creates a sea
    """
    response = client.post(
        "/v1/sea", json={"name": test_data.name, "description": test_data.description}
    )
    assert response.status_code == 201
    assert response.json()["name"] == test_data.name
    assert response.json()["description"] == test_data.description
    assert response.json()["id"].startswith("Sea-")
    test_data.sea_id = response.json()["id"]
    assert sea_models.Sea(**response.json())


def test_get_sea():
    """
    Test that the API returns the correct sea
    """
    response = client.get(f"/v1/sea/{test_data.sea_id}")
    assert response.status_code == 200
    assert response.json()["name"] == test_data.name
    assert response.json()["description"] == test_data.description
    assert response.json()["id"] == test_data.sea_id


def test_get_fish_returns_404():
    """
    Test that the API returns 404 when there are no fish in the sea
    """
    response = client.get(f"/v1/sea/{test_data.sea_id}/fish")
    assert response.status_code == 404


def test_create_fish():
    """
    Test that the API creates a fish
    """
    response = client.post(
        f"/v1/sea/{test_data.sea_id}/fish",
        json={"name": "Nemo", "description": "orange", "data": {}},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Nemo"
    assert response.json()["description"] == "orange"
    assert response.json()["id"].startswith("Fish-")
    test_data.fish_id = response.json()["id"]
    assert response.json()["sea_id"] == test_data.sea_id


def test_get_fish():
    """
    Test that the API returns the correct fish
    """
    response = client.get(f"/v1/sea/{test_data.sea_id}/fish")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Nemo"
    assert response.json()[0]["description"] == "orange"
    assert response.json()[0]["id"] == test_data.fish_id
    assert response.json()[0]["sea_id"] == test_data.sea_id


def test_get_fish_by_id():
    """
    Test that the API returns the correct fish by id
    """
    response = client.get(f"/v1/sea/{test_data.sea_id}/fish/{test_data.fish_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Nemo"
    assert response.json()["description"] == "orange"
    assert response.json()["id"] == test_data.fish_id
    assert response.json()["sea_id"] == test_data.sea_id


def test_delete_fish():
    """
    Test that the API deletes a fish
    """
    response = client.delete(f"/v1/sea/{test_data.sea_id}/fish/{test_data.fish_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Fish deleted successfully."}
    fish_id = None


def test_delete_sea():
    """
    Test that the API deletes a sea
    """
    response = client.delete(f"/v1/sea/{test_data.sea_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Sea deleted successfully."}

    test_data.sea_id = None
