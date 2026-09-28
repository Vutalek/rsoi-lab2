from pydantic import BaseModel


class TicketBuyPost(BaseModel):
    flightNumber: str
    price: int
    paidFromBalance: bool