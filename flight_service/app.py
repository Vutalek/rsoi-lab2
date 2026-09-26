import os
from typing import Annotated

from fastapi import FastAPI, Query, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import construct_engine
from orm import FlightORM

app = FastAPI()

engine = construct_engine()

@app.get("/manage/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/flights")
def all_flights(page: int=1, size: Annotated[int, Query(ge=1, le=100)]=10):
    query = select(FlightORM).order_by(FlightORM.id).limit(size).offset((page-1) * size)
    with Session(engine) as session:
        flights = session.scalars(query).all()
        flights = [
            {
                "flightNumber": flight.flight_number,
                "fromAirport": f"{flight.from_airport.city} {flight.from_airport.name}",
                "toAirport": f"{flight.to_airport.city} {flight.to_airport.name}",
                "date": str(flight.datetime),
                "price": flight.price
            }
            for flight in flights
        ]
    return {
        "page": page,
        "pageSize": size,
        "totalElements": len(flights),
        "items": flights
    }

@app.get("/api/v1/flights/{flight_number}")
def get_flight(flight_number: str):
    query = select(FlightORM).where(FlightORM.flight_number == flight_number)
    with Session(engine) as session:
        flight = session.scalar(query)
        if not flight:
            raise HTTPException(404, detail="Flight not found")
        flight = {
            "flightNumber": flight.flight_number,
            "fromAirport": f"{flight.from_airport.city} {flight.from_airport.name}",
            "toAirport": f"{flight.to_airport.city} {flight.to_airport.name}",
            "date": str(flight.datetime),
            "price": flight.price
        }
    return flight