"""This module simulates private api responses"""
from fastapi import FastAPI
import time
from pydantic import BaseModel

app = FastAPI()


class Payload(BaseModel):
    value: str


@app.post("/")
async def root(payload: Payload):
    """Fake generate response"""
    time.sleep(3)
    return {f"Here is response for your request": payload.value}
