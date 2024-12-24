import pytest
from fastapi.testclient import TestClient

from app.v1.main import app

client = TestClient(app)


def test_1():
    assert 1 == 1
