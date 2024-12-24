import fastapi
import pytest
from fastapi.testclient import TestClient

from app.v1.main import app
from app.v1.routes import fish, sea

client = TestClient(app)

world = world()


class world:
    def __init__(self):
        self.name = "Pacific Ocean"
        self.description = "The largest ocean on Earth."
        self.sea_id = None
        self.fish_id = None


def test_default_redirect():
    response = client.get("/")
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
    response = client.post("/v1/sea", json={"name": name, "description": description})
    assert response.status_code == 201
    assert response.json()["name"] == name
    assert response.json()["description"] == description
    assert response.json()["id"].startswith("Sea-")
    sea_id = response.json()["id"]


def test_get_sea():
    """
    Test that the API returns the correct sea
    """
    response = client.get(f"/v1/sea/{sea_id}")
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["description"] == description
    assert response.json()["id"] == sea_id


def test_get_fish_returns_404():
    """
    Test that the API returns 404 when there are no fish in the sea
    """
    response = client.get(f"/v1/sea/{sea_id}/fish")
    assert response.status_code == 204
    assert response.json()["fish"] == []
    assert response.json()["sea_id"] == sea_id


def test_create_fish():
    """
    Test that the API creates a fish
    """
    response = client.post(
        f"/v1/sea/{sea_id}/fish", json={"name": "Nemo", "color": "orange"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Nemo"
    assert response.json()["color"] == "orange"
    assert response.json()["id"].startswith("Fish-")
    fish_id = response.json()["id"]
    assert response.json()["sea_id"] == sea_id


def test_get_fish():
    """
    Test that the API returns the correct fish
    """
    response = client.get(f"/v1/sea/{sea_id}/fish")
    assert response.status_code == 200
    assert response.json()["fish"][0]["name"] == "Nemo"
    assert response.json()["fish"][0]["color"] == "orange"
    assert response.json()["fish"][0]["id"] == fish_id
    assert response.json()["fish"][0]["sea_id"] == sea_id


def test_get_fish_by_id():
    """
    Test that the API returns the correct fish by id
    """
    response = client.get(f"/v1/sea/{sea_id}/fish/{fish_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Nemo"
    assert response.json()["color"] == "orange"
    assert response.json()["id"] == fish_id
    assert response.json()["sea_id"] == sea_id


def test_delete_fish():
    """
    Test that the API deletes a fish
    """
    response = client.delete(f"/v1/sea/{sea_id}/fish/{fish_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Sea deleted successfully."}
    fish_id = None


def test_delete_sea():
    """
    Test that the API deletes a sea
    """
    response = client.delete(f"/v1/sea/{sea_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Sea deleted successfully."}

    sea_id = None
