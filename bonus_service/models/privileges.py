from pydantic import BaseModel


class PrivilegePost(BaseModel):
    username: str
    status: str | None = None

class PrivilegePatch(BaseModel):
    status: str | None = None
    balance: int | None = None
