from uuid import uuid4


def unique_value(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def register_admin(client):
    email = f"{unique_value('user')}@test.com"
    tenant_name = unique_value("Company")

    response = client.post(
        "/auth/register",
        json={
            "tenant_name": tenant_name,
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201
    return response.json()["access_token"]


def create_product(client, token, sku_prefix="SKU"):
    response = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sku": unique_value(sku_prefix),
            "name": "Test Product",
            "price": "25.50",
        },
    )

    assert response.status_code == 201
    return response


def test_create_product(client):
    token = register_admin(client)

    response = create_product(client, token)

    data = response.json()

    assert data["name"] == "Test Product"
    assert data["price"] == "25.50"
    assert "id" in data


def test_create_duplicate_sku_rejected(client):
    token = register_admin(client)

    sku = unique_value("DUP")

    payload = {
        "sku": sku,
        "name": "Duplicate Product",
        "price": "10.00",
    }

    first = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    second = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_inventory_can_be_retrieved(client):
    token = register_admin(client)

    product_response = create_product(client, token, "INV")

    product_id = product_response.json()["id"]

    response = client.get(
        f"/inventory/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["product_id"] == product_id
    assert response.json()["quantity"] == 0


def test_inventory_can_be_increased(client):
    token = register_admin(client)

    product_response = create_product(client, token, "STOCK")

    product_id = product_response.json()["id"]

    response = client.post(
        f"/inventory/{product_id}/adjust",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "quantity": 10,
            "reason": "Initial stock",
        },
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 10