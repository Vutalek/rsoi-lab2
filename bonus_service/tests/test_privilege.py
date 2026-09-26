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