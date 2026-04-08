def test_post_blacklist_creates_entry(client, auth_header):
    payload = {
        "email": "cliente@empresa.com",
        "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
        "blocked_reason": "fraud",
    }

    response = client.post("/blacklists", json=payload, headers=auth_header)
    data = response.get_json()

    assert response.status_code == 201
    assert data["success"] is True
    assert data["email"] == payload["email"]


def test_post_blacklist_updates_existing_entry(client, auth_header):
    payload = {
        "email": "cliente@empresa.com",
        "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
        "blocked_reason": "first reason",
    }
    client.post("/blacklists", json=payload, headers=auth_header)

    response = client.post(
        "/blacklists",
        json={
            "email": "cliente@empresa.com",
            "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "blocked_reason": "updated reason",
        },
        headers=auth_header,
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["message"] == "The email blacklist entry was updated."


def test_post_blacklist_invalid_payload_returns_400(client, auth_header):
    response = client.post(
        "/blacklists",
        json={"email": "not-an-email", "app_uuid": "not-a-uuid"},
        headers=auth_header,
    )
    data = response.get_json()

    assert response.status_code == 400
    assert "errors" in data
    assert "email" in data["errors"]
    assert "app_uuid" in data["errors"]


def test_post_blacklist_without_token_returns_401(client):
    response = client.post(
        "/blacklists",
        json={
            "email": "cliente@empresa.com",
            "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
        },
    )

    assert response.status_code == 401


def test_get_blacklist_returns_true_for_listed_email(client, auth_header):
    client.post(
        "/blacklists",
        json={
            "email": "listed@empresa.com",
            "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "blocked_reason": "legal request",
        },
        headers=auth_header,
    )

    response = client.get("/blacklists/listed@empresa.com", headers=auth_header)
    data = response.get_json()

    assert response.status_code == 200
    assert data["blacklisted"] is True
    assert data["blocked_reason"] == "legal request"


def test_get_blacklist_returns_false_for_unknown_email(client, auth_header):
    response = client.get("/blacklists/unknown@empresa.com", headers=auth_header)
    data = response.get_json()

    assert response.status_code == 200
    assert data["blacklisted"] is False
    assert data["blocked_reason"] is None


def test_get_blacklist_without_token_returns_401(client):
    response = client.get("/blacklists/unknown@empresa.com")

    assert response.status_code == 401
