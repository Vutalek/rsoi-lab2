from datetime import datetime as dtime

from pydantic import BaseModel

class FlightPost(BaseModel):
    flight_number: str
    datetime: dtime
    from_airport_id: int | None
    to_airport_id: int | None
    price: int