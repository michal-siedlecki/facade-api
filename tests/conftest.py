import pytest
from fastapi.testclient import TestClient
from public import app, PUBLIC_API_KEY


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def data():
    return {"value": "This is test value."}


@pytest.fixture
def api_token():
    return PUBLIC_API_KEY
