def test_get_user_history(client):
    response = client.get("/api/v1/history/1")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "ticket_uid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "datetime": "2026-10-10T20:00:00",
            "balance_diff": 1500,
            "operation_type": "FILL_IN_BALANCE"
        },
        {
            "id": 2,
            "ticket_uid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "datetime": "2026-10-10T20:00:00",
            "balance_diff": 1500,
            "operation_type": "FILL_IN_BALANCE"
        }
    ]

def test_get_entry(client):
    response = client.get("/api/v1/history/entry/1")

    assert response.status_code == 200
    assert response.json() == {
        "privilege_id": 1,
        "ticket_uid": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "datetime": "2026-10-10T20:00:00",
        "balance_diff": 1500,
        "operation_type": "FILL_IN_BALANCE"
    }

def test_increase_balance(client):
    body = {
        "ticket_uid": "cccccccc-cccc-cccc-cccc-cccccccccccc",
        "datetime": "2026-10-13 10:15:00",
        "balance_diff": 100,
        "operation_type": "FILL_IN_BALANCE"
    }

    response = client.post("/api/v1/history/1", json=body)
    assert response.status_code == 201

    response = client.get("/api/v1/privileges/1")
    assert response.json()["balance"] == 1600

def test_decrease_balance(client):
    body = {
        "ticket_uid": "cccccccc-cccc-cccc-cccc-cccccccccccc",
        "datetime": "2026-10-13 10:15:00",
        "balance_diff": 100,
        "operation_type": "DEBIT_THE_ACCOUNT"
    }

    response = client.post("/api/v1/history/1", json=body)
    assert response.status_code == 201

    response = client.get("/api/v1/privileges/1")
    assert response.json()["balance"] == 1400