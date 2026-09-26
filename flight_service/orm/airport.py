from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class AirportORM(Base):
    __tablename__ = "airport"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(255), nullable=True)