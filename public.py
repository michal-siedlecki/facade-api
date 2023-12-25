"""This is the gateway api where user can post a request to the private api.
"""
import requests
import queue
from typing import Any, Optional
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from pymongo import MongoClient


PUBLIC_API_KEY = "1234"
PRIVATE_API_KEY = "1234"
PRIVATE_API_URL = "http://private:8000"
DATABASE_URL = "mongodb://db:27017"
APP_SECRET_KEY = "1234"


app = FastAPI(
    title="Facade",
    openapi_url="/openapi.json",
    secret_key=APP_SECRET_KEY,
    description=__doc__,
    version="0.0.1",
    contact={
        "name": "Michał Siedlecki",
        "email": "siedlecki.michal@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/michal-siedlecki/facade/blob/main/LICENCE",
    },
)


q = queue.Queue()


class TokenModel(BaseModel):
    """The token model which stores"""

    user_key: str
    seconds_used: int
    seconds_limit: int


class Payload(BaseModel):
    """User's payload model"""

    text: str
    binary: Optional[bytes]


def db_context() -> Any:
    """Create database connection"""
    conn = MongoClient(DATABASE_URL)
    collection = conn.tokens["tokens"]
    return collection


@app.post("/")
async def root(
    payload: Payload,
    x_api_header: str = Header(None, convert_underscores=True),
    collection=Depends(db_context),
):
    """Validate input and send request to private api
    also create usage token and return response
    TODO: Warning - api seconds usage is hardcoded
    """
    if not x_api_header:
        raise HTTPException(status_code=403, detail="Forbidden")
    tokens = list(collection.find({"user_key": x_api_header}))
    if not tokens:
        raise HTTPException(status_code=403, detail="Forbidden")
    token_models = [TokenModel(**x) for x in tokens]
    used_seconds = sum([t.seconds_used for t in token_models])
    if not used_seconds < token_models[0].seconds_limit:
        raise HTTPException(status_code=404, detail="Token expired")
    response = requests.post(PRIVATE_API_URL, json={"value": payload.text})
    collection.insert_one(
        {
            "user_key": token_models[0].user_key,
            "seconds_used": 2,
            "seconds_limit": token_models[0].seconds_limit,
        }
    )
    return {"message": response.json()}


@app.post("/create-token")
async def create_token(
    token: TokenModel,
    collection=Depends(db_context),
    X_API_HEADER: str = Header(None, convert_underscores=True),
):
    """Add new token"""
    if X_API_HEADER != APP_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")
    collection.insert_one(dict(token))
    return {"message": "created"}

