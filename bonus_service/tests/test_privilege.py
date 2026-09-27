def test_get_all_privileges(client):
    response = client.get("/api/v1/privileges")

    assert response.status_code == 200
    assert response.json() == {
        "page": 1,
        "pageSize": 10,
        "totalElements": 2,
        "items": [
            {
                "id": 1,
                "username": "vuta",
                "balance": 1500,
                "status": "GOLD"
            },
            {
                "id": 2,
                "username": "vuta2",
                "balance": 2000,
                "status": "BRONZE"
            }
        ]
    }

def test_get_privilege(client):
    response = client.get("/api/v1/privileges/1")

    assert response.status_code == 200
    assert response.json() == {
        "username": "vuta",
        "balance": 1500,
        "status": "GOLD"
    }

def test_post_privilege(client):
    body = {
        "username": "vuta3",
        "status": "SILVER"
    }

    response = client.post("/api/v1/privileges", json=body)

    assert response.status_code == 201
    assert response.headers["location"] == "/api/v1/privileges/3"
    assert response.content == b""

def test_patch_privilege(client):
    body = {"balance": 9999}

    response = client.patch("/api/v1/privileges/1", json=body)
    assert response.status_code == 200

    response = client.get("/api/v1/privileges/1")
    assert response.json()["balance"] == 9999

def test_delete_privilege(client):
    body = {
        "username": "vuta3",
        "status": "SILVER"
    }

    response = client.post("/api/v1/privileges", json=body)
    assert response.status_code == 201

    response = client.delete("/api/v1/privileges/3")
    assert response.status_code == 204

    response = client.get("/api/v1/privileges/3")
    assert response.status_code == 404