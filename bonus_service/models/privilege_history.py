from uuid import UUID
from datetime import datetime as dtime
from typing import Literal

from pydantic import BaseModel

OpTypes = Literal["FILL_IN_BALANCE", "DEBIT_THE_ACCOUNT"]


class HistoryPost(BaseModel):
    ticket_uid: UUID
    datetime: dtime
    balance_diff: int
    operation_type: OpTypes