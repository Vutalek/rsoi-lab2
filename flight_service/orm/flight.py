from datetime import datetime as dtime

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .airport import AirportORM

class FlightORM(Base):
    __tablename__ = "flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_number: Mapped[str] = mapped_column(String(20), nullable=False)
    datetime: Mapped[dtime] = mapped_column(DateTime(timezone=True), nullable=False)
    from_airport_id: Mapped[int | None] = mapped_column(ForeignKey("airport.id"), nullable=True)
    to_airport_id: Mapped[int | None] = mapped_column(ForeignKey("airport.id"), nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    from_airport: Mapped[AirportORM | None] = relationship(foreign_keys=[from_airport_id])
    to_airport: Mapped[AirportORM | None] = relationship(foreign_keys=[to_airport_id])