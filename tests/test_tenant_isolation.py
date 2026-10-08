from uuid import uuid4


def unique_value(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def register_user(client, prefix: str):
    response = client.post(
        "/auth/register",
        json={
            "tenant_name": unique_value(f"{prefix}-company"),
            "email": f"{unique_value(prefix)}@test.com",
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
            "sku": unique_value("ISO-SKU"),
            "name": "Private Product",
            "price": "50.00",
        },
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_tenant_cannot_access_another_tenants_product(client):
    tenant_a_token = register_user(client, "tenant-a")
    tenant_b_token = register_user(client, "tenant-b")

    product_id = create_product(client, tenant_a_token)

    response = client.get(
        f"/inventory/{product_id}",
        headers={"Authorization": f"Bearer {tenant_b_token}"},
    )

    assert response.status_code == 404


def test_tenant_cannot_create_order_for_another_tenants_product(client):
    tenant_a_token = register_user(client, "order-a")
    tenant_b_token = register_user(client, "order-b")

    product_id = create_product(client, tenant_a_token)

    response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {tenant_b_token}"},
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1,
                }
            ]
        },
    )

    assert response.status_code == 404