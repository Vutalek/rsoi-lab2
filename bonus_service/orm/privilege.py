from typing import Literal

from sqlalchemy import CheckConstraint, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

PrivilegeLevel = Literal["BRONZE", "SILVER", "GOLD"]

class PrivilegeORM(Base):
    __tablename__ = "privilege"

    __table_args__ = (
        CheckConstraint(
            "status IN ('BRONZE', 'SILVER', 'GOLD')",
            name="privilege_status_check",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    status: Mapped[PrivilegeLevel] = mapped_column(String(80), default="BRONZE", nullable=False)
    balance: Mapped[int] = mapped_column(Integer)