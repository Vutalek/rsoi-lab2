from datetime import datetime as dtime

from pydantic import BaseModel

class AirportPost(BaseModel):
    name: str
    city: str
    country: str

class AirportPatch(BaseModel):
    name: str | None = None
    city: str | None = None
    country: str | None = None