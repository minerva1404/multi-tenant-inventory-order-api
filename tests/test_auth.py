def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "tenant_name": "Test Company",
            "email": "admin@testcompany.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]


def test_login(client):
    client.post(
        "/auth/register",
        json={
            "tenant_name": "Login Company",
            "email": "login@testcompany.com",
            "password": "StrongPassword123!",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "login@testcompany.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]


def test_login_with_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "tenant_name": "Wrong Password Company",
            "email": "wrong@testcompany.com",
            "password": "StrongPassword123!",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong@testcompany.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_duplicate_email(client):
    payload = {
        "tenant_name": "Duplicate Company",
        "email": "duplicate@testcompany.com",
        "password": "StrongPassword123!",
    }

    first = client.post("/auth/register", json=payload)
    second = client.post("/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409