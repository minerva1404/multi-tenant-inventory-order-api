# Multi-Tenant Inventory & Order API

A FastAPI backend demonstrating multi-tenant SaaS architecture, JWT authentication, role-based access control, inventory management, transactional orders, concurrency-safe inventory updates, database migrations, automated testing, Docker containerization, CI, and cloud deployment.

## Stack

- Python 3.12

- FastAPI

- SQLAlchemy

- PostgreSQL

- Psycopg

- Alembic

- JWT

- Argon2

- pytest

- Ruff

- Docker

- GitHub Actions

- Supabase

- Render

## Live Demo

- API: YOUR_RENDER_URL

- Swagger UI: YOUR_RENDER_URL/docs

- Health Check: YOUR_RENDER_URL/health

## Local Setup

1. Create and activate a virtual environment.

2. Install dependencies:

```bash

pip install -r requirements.txt

```

3. Create `.env` from `.env.example` and configure the PostgreSQL connection string and JWT settings.

4. Apply migrations:

```bash

alembic upgrade head

```

5. Run the application:

```bash

uvicorn app.main:app --reload

```

Open `/docs` for Swagger UI.

## Main Endpoints

- `POST /auth/register`

- `POST /auth/login`

- `POST /products`

- `GET /products`

- `GET /inventory/{product_id}`

- `POST /inventory/{product_id}/adjust`

- `POST /orders`

- `GET /orders/{order_id}`

- `GET /health`

## Tenant Isolation

JWTs carry both `user_id` and `tenant_id`. Every tenant-owned query includes the authenticated tenant ID.

Order creation locks inventory rows before decrementing stock, preventing concurrent orders from overselling the same inventory.

## Roles

- `admin`: create products and adjust inventory

- `member`: read products and inventory and create/read orders

## Database

PostgreSQL is hosted on Supabase and managed through SQLAlchemy and Alembic migrations.

## Testing

The project includes automated tests covering authentication, tenant isolation, products, inventory, orders, health checks, and core API behavior.

Current test result:

```text

15 passed

```

Run the test suite with:

```bash

pytest

```

## Code Quality

Ruff is used for linting.

```bash

ruff check .

```

## Docker

Build the Docker image:

```bash

docker build -t multi-tenant-inventory-api .

```

Run the container:

```bash

docker run --rm --env-file .env -p 8000:8000 multi-tenant-inventory-api

```

## CI/CD

GitHub Actions runs the automated test and code-quality checks.

The application is containerized with Docker and deployed as a public web service on Render.

## Security

- `.env` is excluded from version control

- Secrets are supplied through environment variables

- Passwords are hashed using Argon2

- JWT authentication protects authenticated endpoints

- Tenant IDs are enforced at the application layer

- Role-based permissions restrict administrative operations

## Repository

GitHub:

https://github.com/minerva1404/multi-tenant-inventory-order-api


