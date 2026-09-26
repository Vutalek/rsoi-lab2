import uuid
from datetime import datetime as dtime
from typing import Literal

from sqlalchemy import CheckConstraint, ForeignKey, DateTime, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

OpTypes = Literal["FILL_IN_BALANCE", "DEBIT_THE_ACCOUNT"]

class PrivilegeHistoryORM(Base):
    __tablename__ = "privilege_history"

    __table_args__ = (
        CheckConstraint(
            "operation_type IN ('FILL_IN_BALANCE', 'DEBIT_THE_ACCOUNT')",
            name="privilege_history_optype_check",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    privilege_id: Mapped[int] = mapped_column(ForeignKey("privilege.id"), nullable=True)
    ticket_uid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    datetime: Mapped[dtime] = mapped_column(DateTime(timezone=True), nullable=False)
    balance_diff: Mapped[int] = mapped_column(Integer, nullable=False)
    operation_type: Mapped[OpTypes] = mapped_column(String(20), nullable=False)