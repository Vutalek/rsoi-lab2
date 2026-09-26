def test_get_flights(client):
    response = client.get("/api/v1/flights")

    assert response.status_code == 200
    assert response.json() == {
        "page": 1,
        "pageSize": 10,
        "totalElements": 1,
        "items": [
            {
                "flightNumber": "AFL031",
                "fromAirport": "Санкт-Петербург Пулково",
                "toAirport": "Москва Шереметьево",
                "date": "2026-10-08 20:00:00",
                "price": 1500
            }
        ]
    }

def test_create_flight(client):
    body = {
        "flight_number": "LFA130",
        "datetime": "2026-10-15 18:00",
        "from_airport_id": 1,
        "to_airport_id": 2,
        "price": 2000,
    }

    response = client.post(
        "/api/v1/flights",
        json=body
    )

    assert response.status_code == 201

    assert response.headers["location"] == "/api/v1/flights/LFA130"

    assert response.content == b""

def test_patch_flight(client):
    body = {
        "flight_number": "AFL130",
        "datetime": "2026-10-08 20:00",
        "from_airport_id": 1,
        "to_airport_id": 2,
        "price": 1500,
    }

    response = client.post(
        "/api/v1/flights",
        json=body
    )
    
    body = {
        "price": 2000
    }

    response = client.patch(
        "/api/v1/flights/AFL130",
        json=body
    )

    assert response.status_code == 200

    assert response.json().get("price") == 2000

def test_delete_flight(client):
    body = {
        "flight_number": "AFL130",
        "datetime": "2026-10-08 20:00",
        "from_airport_id": 1,
        "to_airport_id": 2,
        "price": 1500,
    }

    response = client.post(
        "/api/v1/flights",
        json=body
    )

    response = client.get("/api/v1/flights/AFL130")

    assert response.status_code == 200

    response = client.delete("/api/v1/flights/AFL130")

    assert response.status_code == 200

    response = client.get("/api/v1/flights/AFL130")

    assert response.status_code == 404