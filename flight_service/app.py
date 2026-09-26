import os
from typing import Annotated

from fastapi import FastAPI, Query, HTTPException, Response, status

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from utils import construct_engine
from orm import FlightORM
from models import FlightPost, FlightPatch

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

@app.post("/api/v1/flights")
def make_flight(body: FlightPost):
    get_next_id = select(
        (func.coalesce(func.max(FlightORM.id), 0) + 1)
    )
    with Session(engine) as session:
        next_id = session.scalar(get_next_id)

        new_flight = FlightORM(
            id=next_id,
            flight_number=body.flight_number,
            datetime=body.datetime,
            from_airport_id=body.from_airport_id,
            to_airport_id=body.to_airport_id,
            price=body.price
        )
        session.add(new_flight)
        session.commit()
        return Response(
            status_code=status.HTTP_201_CREATED,
            headers={
                "Location": f"/api/v1/flights/{body.flight_number}"
            }
    )

@app.patch("/api/v1/flights/{flight_number}")
def update_flight(flight_number: str, body: FlightPatch):
    get_flight = select(FlightORM).where(FlightORM.flight_number == flight_number)
    with Session(engine) as session:
        flight = session.scalar(get_flight)
        if not flight:
            raise HTTPException(404, detail="Flight not found")
        for field, value in body.model_dump(exclude_unset=True).items():
            setattr(flight, field, value)

        session.commit()
        session.refresh(flight)
    return flight