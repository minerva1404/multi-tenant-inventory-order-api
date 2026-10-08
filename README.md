# Multi-Tenant Inventory & Order API

A FastAPI backend demonstrating tenant isolation, JWT authentication, RBAC, inventory management, transactional orders, and row-level locking.

## Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- MySQL
- PyMySQL
- JWT
- Argon2
- pytest
- Ruff
- Docker

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and set your MySQL credentials.
4. Apply migrations:

```bash
alembic upgrade head
```

5. Run:

```bash
uvicorn app.main:app --reload
```

Open `/docs` for Swagger UI.

## Main endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /products`
- `GET /products`
- `GET /inventory/{product_id}`
- `POST /inventory/{product_id}/adjust`
- `POST /orders`
- `GET /orders/{order_id}`
- `GET /health`

## Tenant isolation

JWTs carry both `user_id` and `tenant_id`. Every tenant-owned query includes the authenticated tenant ID. Order creation locks inventory rows before decrementing stock, preventing two concurrent orders from overselling the same inventory row.

## Roles

- `admin`: create products and adjust inventory
- `member`: read products/inventory and create/read orders

## Security

Never commit `.env`. Use `.env.example` as the safe template.
