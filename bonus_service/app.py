from uuid import UUID, uuid4
from typing import Annotated

from fastapi import FastAPI, Query, HTTPException, Response, status

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from utils import construct_engine
from orm import PrivilegeORM, PrivilegeHistoryORM

app = FastAPI()

engine = construct_engine()

@app.get("/manage/health")
def health():
    return {"status": "healthy"}

###############################
########## Privilege ##########
###############################

@app.get("/api/v1/privileges")
def all_privileges(page: int=1, size: Annotated[int, Query(ge=1, le=100)]=10):
    query = select(PrivilegeORM).order_by(PrivilegeORM.id).limit(size).offset((page-1) * size)
    with Session(engine) as session:
        privileges = session.scalars(query).all()
    privileges = [
        {
            "id": privilege.id,
            "username": privilege.username,
            "balance": privilege.balance,
            "status": privilege.status
        }
        for privilege in privileges
    ]
    return {
        "page": page,
        "pageSize": size,
        "totalElements": len(privileges),
        "items": privileges
    }

@app.get("/api/v1/privileges/{p_id}")
def get_privilege(p_id: int):
    with Session(engine) as session:
        privilege = session.get(PrivilegeORM, p_id)
        if not privilege:
            raise HTTPException(404, detail="Privilege not found")
    privilege = {
        "username": privilege.username,
        "balance": privilege.balance,
        "status": privilege.status
    }
    return privilege

#######################################
########## Privilege History ##########
#######################################

@app.get("/api/v1/history/{p_id}")
def get_history(p_id: int):
    query = select(PrivilegeHistoryORM).where(PrivilegeHistoryORM.privilege_id == p_id)
    with Session(engine) as session:
        history = session.scalars(query).all()
    history = [
        {
            "id": h.id,
            "ticket_uid": h.ticket_uid,
            "datetime": h.datetime,
            "balance_diff": h.balance_diff,
            "operation_type": h.operation_type
        }
        for h in history
    ]
    return history