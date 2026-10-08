\# Multi-Tenant Inventory \& Order API



A production-style multi-tenant B2B SaaS backend built with FastAPI and PostgreSQL.



This project demonstrates JWT authentication, role-based access control, tenant isolation, inventory management, transactional order processing, concurrency-safe inventory updates, database migrations, automated testing, Docker containerization, CI, and cloud deployment.



\## Live Demo



\*\*API:\*\* https://multi-tenant-inventory-order-api.onrender.com


\*\*Swagger UI:\*\* \https://multi-tenant-inventory-order-api.onrender.com/docs



\*\*Health Check:\*\* https://multi-tenant-inventory-order-api.onrender.com/health



\## Architecture



```text

Client

&#x20; ↓

FastAPI

&#x20; ↓

JWT Authentication + RBAC

&#x20; ↓

Tenant-Aware Business Logic

&#x20; ↓

SQLAlchemy ORM

&#x20; ↓

PostgreSQL (Supabase)

```



The application is containerized with Docker and deployed as a public web service.



\## Tech Stack



\- Python 3.12

\- FastAPI

\- SQLAlchemy

\- PostgreSQL

\- Psycopg

\- Alembic

\- JWT / PyJWT

\- Argon2 password hashing

\- pytest

\- Ruff

\- Docker

\- GitHub Actions

\- Supabase

\- Render



\## Core Features



\### Authentication \& Authorization



\- JWT-based authentication

\- Secure password hashing with Argon2

\- Role-based access control

\- Admin and member roles

\- Token-based tenant identification



\### Multi-Tenancy



Each user belongs to a tenant.



Tenant-owned database operations are scoped using the authenticated tenant ID, preventing users from accessing another tenant's data.



\### Product Management



\- Create products

\- List products

\- Tenant-scoped product access

\- Automatic inventory record creation



\### Inventory Management



\- View inventory

\- Adjust stock quantities

\- Track inventory movements

\- Admin-only inventory adjustments



\### Order Management



\- Create orders

\- Retrieve orders

\- Transactional inventory updates

\- Inventory row locking to prevent concurrent overselling

\- Order and order-item persistence



\## Database



\- PostgreSQL hosted on Supabase

\- Alembic database migrations

\- Transactional schema changes

\- Database health validation



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| POST | `/auth/register` | Register a new tenant and user |

| POST | `/auth/login` | Authenticate and receive a JWT |

| POST | `/products` | Create a product |

| GET | `/products` | List products |

| GET | `/inventory/{product\_id}` | View product inventory |

| POST | `/inventory/{product\_id}/adjust` | Adjust inventory |

| POST | `/orders` | Create an order |

| GET | `/orders/{order\_id}` | Retrieve an order |

| GET | `/health` | Check API and database health |



Interactive API documentation is available through Swagger UI at `/docs`.



\## Testing



The project includes automated tests covering:



\- Authentication

\- Product management

\- Inventory management

\- Order creation

\- Order retrieval

\- Tenant isolation

\- API health

\- Core application behavior



Current test result:



```text

15 passed

```



Run the test suite locally:



```bash

pytest

```



\## Code Quality



Ruff is used for linting.



```bash

ruff check .

```



\## Database Migrations



Apply the latest migrations:



```bash

alembic upgrade head

```



\## Docker



Build the Docker image:



```bash

docker build -t multi-tenant-inventory-api .

```



Run the container:



```bash

docker run --rm --env-file .env -p 8000:8000 multi-tenant-inventory-api

```



The container runs the database migrations before starting the FastAPI application.



\## Local Setup



\### 1. Clone the repository



```bash

git clone https://github.com/minerva1404/multi-tenant-inventory-order-api.git

cd multi-tenant-inventory-order-api

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows:



```powershell

.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure environment variables



Create `.env` from `.env.example`.



Set:



```text

DATABASE\_URL=your-postgresql-connection-string

JWT\_SECRET=your-secret-key

JWT\_ALGORITHM=HS256

ACCESS\_TOKEN\_EXPIRE\_MINUTES=30

```



Never commit the `.env` file.



\### 5. Run migrations



```bash

alembic upgrade head

```



\### 6. Start the API



```bash

uvicorn app.main:app --reload

```



Open:



```text

http://127.0.0.1:8000/docs

```



\## CI/CD



GitHub Actions automatically runs:



\- Dependency installation

\- Ruff linting

\- pytest test suite



Every push to `main` and every pull request targeting `main` triggers the CI workflow.



The application is containerized with Docker and deployed through Render.



\## Security



\- `.env` is excluded from version control

\- Secrets are supplied through environment variables

\- Passwords are hashed using Argon2

\- JWT authentication protects authenticated endpoints

\- Tenant IDs are enforced at the application layer

\- Role-based permissions restrict administrative operations



\## Repository



GitHub:



https://github.com/minerva1404/multi-tenant-inventory-order-api

