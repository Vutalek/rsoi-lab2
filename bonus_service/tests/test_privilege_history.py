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