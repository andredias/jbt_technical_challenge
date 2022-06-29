from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


Coords = tuple[float, float]


class Destination(BaseModel):
    time: datetime
    coords: Coords
