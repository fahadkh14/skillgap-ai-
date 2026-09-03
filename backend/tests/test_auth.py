def test_register_success(client):
    resp = client.post(
        "/api/auth/register",
        json={
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "password": "SecurePass123",
            "confirm_password": "SecurePass123",
        },
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"] is True
    assert "access_token" in data["data"]


def test_register_duplicate_email_rejected(client):
    payload = {
        "full_name": "Jane Doe",
        "email": "dupe@example.com",
        "password": "SecurePass123",
        "confirm_password": "SecurePass123",
    }
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 409


def test_register_password_mismatch(client):
    resp = client.post(
        "/api/auth/register",
        json={
            "full_name": "Jane Doe",
            "email": "jane2@example.com",
            "password": "SecurePass123",
            "confirm_password": "Different123",
        },
    )
    assert resp.status_code == 422


def test_login_success(client, registered_user):
    resp = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123",
        },
    )
    assert resp.status_code == 200
    assert resp.get_json()["data"]["access_token"]


def test_login_invalid_credentials(client, registered_user):
    resp = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword",
        },
    )
    assert resp.status_code == 401


def test_protected_route_requires_auth(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_protected_route_with_valid_token(client, auth_headers):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["data"]["email"] == "test@example.com"
