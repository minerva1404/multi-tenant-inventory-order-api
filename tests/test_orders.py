from uuid import uuid4


def unique_value(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def register_admin(client):
    response = client.post(
        "/auth/register",
        json={
            "tenant_name": unique_value("OrderCompany"),
            "email": f"{unique_value('order')}@test.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 201
    return response.json()["access_token"]


def create_product(client, token):
    response = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sku": unique_value("ORDER-SKU"),
            "name": "Order Test Product",
            "price": "25.00",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def add_inventory(client, token, product_id, quantity):
    response = client.post(
        f"/inventory/{product_id}/adjust",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "quantity": quantity,
            "reason": "Order test stock",
        },
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == quantity


def test_create_order_reduces_inventory(client):
    token = register_admin(client)
    product_id = create_product(client, token)

    add_inventory(client, token, product_id, 10)

    response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 3,
                }
            ]
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "confirmed"
    assert data["total_amount"] == "75.00"
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == product_id
    assert data["items"][0]["quantity"] == 3
    assert data["items"][0]["unit_price"] == "25.00"
    assert data["items"][0]["line_total"] == "75.00"

    inventory_response = client.get(
        f"/inventory/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert inventory_response.status_code == 200
    assert inventory_response.json()["quantity"] == 7


def test_order_rejected_when_inventory_is_insufficient(client):
    token = register_admin(client)
    product_id = create_product(client, token)

    add_inventory(client, token, product_id, 2)

    response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 5,
                }
            ]
        },
    )

    assert response.status_code == 409
    assert "Insufficient inventory" in response.json()["detail"]


def test_duplicate_product_in_order_is_rejected(client):
    token = register_admin(client)
    product_id = create_product(client, token)

    add_inventory(client, token, product_id, 10)

    response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                },
                {
                    "product_id": product_id,
                    "quantity": 1,
                },
            ]
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Each product can appear only once per order"
    )