from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from public import app, PUBLIC_API_KEY, db_context


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def data():
    return {"text": "string", "binary": "string"}


@pytest.fixture
def user_token():
    token = str(uuid4())
    collection = db_context()
    collection.insert_one({"user_key": token, "seconds_used": 0, "seconds_limit": 4})
    return token


@pytest.fixture
def api_token():
    return PUBLIC_API_KEY
