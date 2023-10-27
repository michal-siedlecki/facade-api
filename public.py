"""This is the gateway where user can post a request to the private api using the public gateway
"""
import requests
import queue
from fastapi import FastAPI
from pydantic import BaseModel

PUBLIC_API_KEY = "1234"
PRIVATE_API_KEY = "1234"
PRIVATE_API_URL = "http://private:8000"
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


class Payload(BaseModel):
    value: str


@app.get("/")
async def root():
    return {"message": "Hello World, please send a request"}


@app.post("/")
async def root(payload: Payload):
    """Send request to private api and return response
    TODO: add validation
    TODO: push the prompt to redis queue
    """
    response = requests.post(PRIVATE_API_URL, json={"value": payload.value})
    return {"message": response.json()}
