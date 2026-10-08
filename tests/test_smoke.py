from fastapi.testclient import TestClient


def test_root(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert "API is running" in response.json()["message"]


def test_health(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "connected"