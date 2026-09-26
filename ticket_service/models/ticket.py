from pydantic import BaseModel


class TicketPost(BaseModel):
    username: str
    flight_number: str
    price: int