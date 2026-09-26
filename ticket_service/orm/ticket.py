import uuid
from typing import Literal

from sqlalchemy import CheckConstraint, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

TicketStatus = Literal["PAID", "CANCELED"]

class TicketORM(Base):
    __tablename__ = "ticket"

    __table_args__ = (
        CheckConstraint(
            "status IN ('PAID', 'CANCELED')",
            name="ticket_status_check",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    flight_number: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(String(20), nullable=False)