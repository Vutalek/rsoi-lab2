def test_get_airports(client):
    response = client.get("/api/v1/airports")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Шереметьево",
            "city": "Москва",
            "country": "Россия"
        },
        {
            "id": 2,
            "name": "Пулково",
            "city": "Санкт-Петербург",
            "country": "Россия"
        }
    ]

def test_create_airport(client):
    body = {
        "name": "Ханеда",
        "city": "Токио",
        "country": "Япония"
    }

    response = client.post(
        "/api/v1/airports",
        json=body
    )

    assert response.status_code == 201

    assert response.headers["location"] == "/api/v1/airports/3"

    assert response.content == b""

def test_patch_airport(client):
    body = {
        "name": "Ханеда",
        "city": "Токио",
        "country": "Япония"
    }

    response = client.post(
        "/api/v1/airports",
        json=body
    )
    
    body = {
        "country": "ЯПОНИЯ"
    }

    response = client.patch(
        "/api/v1/airports/3",
        json=body
    )

    assert response.status_code == 200

    assert response.json().get("country") == "ЯПОНИЯ"

def test_delete_airport(client):
    body = {
        "name": "Ханеда",
        "city": "Токио",
        "country": "Япония"
    }

    response = client.post(
        "/api/v1/airports",
        json=body
    )

    response = client.get("/api/v1/airports/3")

    assert response.status_code == 200

    response = client.delete("/api/v1/airports/3")

    assert response.status_code == 204

    response = client.get("/api/v1/airports/3")

    assert response.status_code == 404