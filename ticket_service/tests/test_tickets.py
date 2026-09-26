def test_get_tickets_by_user(client):
    response = client.get("/api/v1/tickets/user/vuta")

    assert response.status_code == 200
    assert response.json() == [
        {
            "ticketUid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "flightNumber": "AFL031",
            "price": 1500,
            "status": "PAID",
        }
    ]

def test_get_ticket(client):
    response = client.get("/api/v1/tickets/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")

    assert response.status_code == 200
    assert response.json() == {
        "username": "vuta",
        "flightNumber": "AFL031",
        "price": 1500,
        "status": "PAID",
    }

def test_buy_ticket(client):
    body = {
        "username": "vuta",
        "flight_number": "LFA130",
        "price": 2000
    }

    response = client.post(
        "/api/v1/tickets",
        json=body
    )

    assert response.status_code == 201

    assert response.headers["location"].startswith("/api/v1/tickets/")

    assert response.content == b""

def test_cancel_ticket(client):
    body = {
        "username": "vuta",
        "flight_number": "LFA130",
        "price": 2000
    }
    
    response = client.post(
        "/api/v1/tickets",
        json=body
    )

    uid = response.headers["location"].split('/')[-1]

    response = client.get(f"/api/v1/tickets/{uid}")

    assert response.json().get("status") == "PAID"

    response = client.post(f"/api/v1/tickets/cancel/{uid}")

    assert response.json().get("status") == "CANCELED"

    response = client.get(f"/api/v1/tickets/{uid}")
    
    assert response.json().get("status") == "CANCELED"