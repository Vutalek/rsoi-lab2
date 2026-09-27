import os
from uuid import UUID
from datetime import datetime as dtime
from typing import Annotated

import requests
from fastapi import FastAPI, Query, Header, HTTPException, Response, status

from models import TicketBuyPost

app = FastAPI()
flight_service = os.environ.get("FLIGHT_SERVICE_HOST", "")
ticket_service = os.environ.get("TICKET_SERVICE_HOST", "")
bonus_service = os.environ.get("BONUS_SERVICE_HOST", "")


@app.get("/api/v1/flights")
def get_all_flights(page: int=1, size: Annotated[int, Query(ge=1, le=100)]=10):
    return requests.get(flight_service + f"/api/v1/flights?page={page}&size={size}").json()

@app.get("/api/v1/tickets")
def get_all_user_tickets(x_user_name: Annotated[str, Header()]):
    tickets = requests.get(ticket_service + f"/api/v1/tickets/user/{x_user_name}").json()
    extended_tickets = []
    for ticket in tickets:
        flight = requests.get(flight_service + f"/api/v1/flights/{ticket.get('flightNumber', '')}").json()
        extended_tickets.append(
            {
                "ticketUid": ticket.get("ticketUid"),
                "flightNumber": flight.get("flightNumber", ""),
                "fromAirport": flight.get("fromAirport", ""),
                "toAirport": flight.get("toAirport", ""),
                "date": flight.get("date", ""),
                "price": flight.get("price", ""),
                "status": ticket.get("status", "")
            }
        )
    return extended_tickets

@app.post("/api/v1/tickets")
def buy_ticket(x_user_name: Annotated[str, Header()], body: TicketBuyPost):
    # создаём билет
    ticket_uid = requests.post(
        ticket_service + "/api/v1/tickets",
        body = {
            "username": x_user_name,
            "flight_number": body.flightNumber,
            "price": body.price
        }
    ).headers["Location"].split('/')[-1]

    # получаем бонусный счёт пользователя
    privilege = requests.get(bonus_service + f"/api/v1/privileges/user/{x_user_name}")
    current_datetime = dtime.now().isoformat(sep=' ')

    # проводим расчёт бонусов
    if body.paidFromBalance & privilege.status_code == 200:
        difference = body.price - privilege.json().get("balance", 0)
        if difference <= 0:
            balance_diff = body.price
            paid_by_money = 0
            paid_by_bonuses = body.price
        else:
            balance_diff = privilege.json().get("balance", 0)
            paid_by_money = difference
            paid_by_bonuses = privilege.json().get("balance", 0)
        requests.post(
            bonus_service + f"/api/v1/history/{privilege.json().get('id')}",
            body = {
                "ticket_uid": ticket_uid,
                "datetime": current_datetime,
                "balance_diff": balance_diff,
                "operation_type": "DEBIT_THE_ACCOUNT"
            }
        )
    else:
        requests.post(
            bonus_service + f"/api/v1/history/{privilege.json().get('id')}",
            body = {
                "ticket_uid": ticket_uid,
                "datetime": current_datetime,
                "balance_diff": int(body.price * 0.1),
                "operation_type": "FILL_IN_BALANCE"
            }
        )
        paid_by_money = body.price
        paid_by_bonuses = 0

    # меняем статус билета
    requests.post(ticket_service + f"/api/v1/tickets/pay/{ticket_uid}")

    # собираем всю информацию по билету
    flight = requests.get(flight_service + f"/api/v1/flights/{body.flightNumber}").json()
    current_privilege = privilege = requests.get(bonus_service + f"/api/v1/privileges/user/{x_user_name}").json()
    response = {
        "ticketUid": ticket_uid,
        "flightNumber": flight.get("flightNumber", ""),
        "fromAirport": flight.get("fromAirport", ""),
        "toAirport": flight.get("toAirport", ""),
        "date": flight.get("date", ""),
        "price": flight.get("price", ""),
        "paidByMoney": paid_by_money,
        "paidByBonuses": paid_by_bonuses,
        "status": "PAID",
        "privilege": {
            "balance": current_privilege.get("balance", 0),
            "status": current_privilege.get("status", "BRONZE")
        }
    }
    return response

@app.get("/api/v1/tickets/{ticket_uid}")
def get_ticket(ticket_uid: UUID, x_user_name: Annotated[str, Header()]):
    ticket = requests.get(ticket_service + f"/api/v1/tickets/{ticket_uid}")
    if ticket.status_code == 404:
        raise HTTPException("Ticket not found!")
    ticket = ticket.json()

    flight = requests.get(flight_service + f"/api/v1/flights/{ticket.get('flightNumber', '')}").json()

    response = {
        "ticketUid": ticket_uid,
        "flightNumber": flight.get("flightNumber", ""),
        "fromAirport": flight.get("fromAirport", ""),
        "toAirport": flight.get("toAirport", ""),
        "date": flight.get("date", ""),
        "price": flight.get("price", ""),
        "status": ticket.get("status", "")
    }
    return response

@app.delete("/api/v1/tickets/{ticket_uid}")
def get_ticket(ticket_uid: UUID, x_user_name: Annotated[str, Header()]):
    response = requests.post(ticket_service + f"/api/v1/tickets/cancel/{ticket_uid}")
    if response.status_code == 204:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException("Ticket not found")

@app.get("/api/v1/me")
def get_me(x_user_name: Annotated[str, Header()]):
    tickets = requests.get(ticket_service + f"/api/v1/tickets/user/{x_user_name}").json()
    extended_tickets = []
    for ticket in tickets:
        flight = requests.get(flight_service + f"/api/v1/flights/{ticket.get('flightNumber', '')}").json()
        extended_tickets.append(
            {
                "ticketUid": ticket.get("ticketUid"),
                "flightNumber": flight.get("flightNumber", ""),
                "fromAirport": flight.get("fromAirport", ""),
                "toAirport": flight.get("toAirport", ""),
                "date": flight.get("date", ""),
                "price": flight.get("price", ""),
                "status": ticket.get("status", "")
            }
        )

    privilege = requests.get(bonus_service + f"/api/v1/privileges/user/{x_user_name}").json()

    response = {
        "tickets": extended_tickets,
        "privilege": {
            "balance": privilege.get("balance"),
            "status": privilege.get("status")
        }
    }
    return response

@app.get("/api/v1/privilege")
def get_privilege(x_user_name: Annotated[str, Header()]):
    privilege = requests.get(bonus_service + f"/api/v1/privileges/user/{x_user_name}").json()
    history = requests.get(bonus_service + f"/api/v1/history/{privilege.get('id', '')}").json()

    response = {
        "balance": privilege.get("balance"),
        "status": privilege.get("status"),
        "history": [
            {
                "date": h.get("date", ""),
                "ticketUid": h.get("ticket_uid", ""),
                "balanceDiff": h.get("balance_diff", 0),
                "operationType": h.get("operation_type", "")
            }
            for h in history
        ]
    }
    return response