from typing import Literal

from pydantic import BaseModel

PrivilegeLevel = Literal["BRONZE", "SILVER", "GOLD"]


class PrivilegePost(BaseModel):
    username: str
    status: PrivilegeLevel | None = None

class PrivilegePatch(BaseModel):
    status: PrivilegeLevel | None = None
    balance: int | None = None
