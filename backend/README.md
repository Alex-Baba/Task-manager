# Backend

FastAPI backend for a task management application with authentication, admin access,
user-owned tasks and tags, seeded categories, and ML-assisted task predictions.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy async
- PostgreSQL
- Alembic
- Pydantic
- JWT authentication
- scikit-learn model loading for category prediction
- pytest + httpx for integration tests

## Project Structure

```text
app/
  api/              FastAPI routers and dependencies
  core/             config, security, enums, custom exceptions
  db/               database session setup
  ml/               prediction text builder, model loader, scoring logic
  models/           SQLAlchemy models
  repositories/     database access layer
  schemas/          Pydantic request/response schemas
  services/         business logic
migrations/         Alembic migrations
scripts/            seed scripts
tests/              integration tests
```

## Environment Variables

The backend expects these variables:

```env
DATABASE_URL=postgresql+asyncpg://<db_user>:<db_password>@<db_host>:5432/<db_name>
TEST_DATABASE_URL=postgresql+asyncpg://<db_user>:<db_password>@<db_host>:5432/<test_db_name>

SECRET_KEY=change-this-value
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ADMIN_EMAIL=<admin_email>
ADMIN_USERNAME=<admin_username>
ADMIN_PASSWORD=<admin_password>
```

`DATABASE_URL` is used by the application. `TEST_DATABASE_URL` must point to a
separate database because the test suite recreates the schema.

## Running With Docker

From the repository root:

```powershell
docker compose up -d --build
```

The backend is available at:

```text
http://localhost:8000
```

Interactive FastAPI docs are available at:

```text
http://localhost:8000/docs
```

ReDoc documentation is available at:

```text
http://localhost:8000/redoc
```

Swagger UI is useful for testing requests from the browser, while ReDoc offers a
cleaner read-only API documentation view.

The backend container runs Alembic migrations automatically on startup, then seeds
reference categories and the initial admin user if the admin environment variables
are configured.

## Database Migrations

Run migrations manually from inside the backend container:

```powershell
docker compose exec backend alembic upgrade head
```

Create a new migration:

```powershell
docker compose exec backend alembic revision --autogenerate -m "migration message"
```

## Seed Scripts

Seed categories:

```powershell
docker compose exec backend python -m scripts.seed_categories
```

Seed the initial admin user from environment variables:

```powershell
docker compose exec backend python -m scripts.seed_admin
```

## Tests

Run the backend test suite:

```powershell
docker compose exec backend pytest
```

The tests use `TEST_DATABASE_URL`. The database configured there is dropped and
recreated during test setup, so it must not be the development database.

The Docker Compose setup mounts `docker/postgres/init-test-db.sh` into the
PostgreSQL container. When the database volume is initialized for the first time,
the script creates the test database configured through `POSTGRES_TEST_DB`.

If the PostgreSQL volume already exists, create the test database manually:

```powershell
docker compose exec db createdb -U licenta_user test_db
```

Current test coverage includes:

- user registration, login, and current user profile
- admin-only access
- granting and revoking admin role
- seeded public categories
- task creation defaults
- user ownership boundaries
- tag creation and task assignment
- prediction generation and application
- validation errors
- full end-to-end task prediction flow

## Authentication

The API uses JWT access tokens.

Login endpoint:

```text
POST /auth/login
```

Current user endpoint:

```text
GET /auth/me
```

JWT tokens contain only `sub` and `exp`. User data and admin status are returned
by `/auth/me`.

## Main API Areas

```text
/auth          login and current user
/users         user self-management
/admin         admin-only operations
/categories    public category reads
/tags          user-owned tags
/tasks         user-owned tasks
/tasks/{id}/predictions    ML prediction flow
/health        application health
/test-db       database connectivity check
```

## Prediction Flow

The prediction flow is designed as a suggestion system:

1. A user creates a task.
2. The user requests a prediction for that task.
3. The backend uses the ML model to suggest a category and priority.
4. The prediction is stored as the active prediction for the task.
5. The user can apply the suggested category, priority, or both.
6. Applied fields are tracked with `applied_category`, `applied_priority`, and
   `applied_at`.

Important endpoints:

```text
POST /tasks/{task_id}/predictions/generate
GET  /tasks/{task_id}/predictions/active
GET  /tasks/{task_id}/predictions
POST /tasks/{task_id}/predictions/{prediction_id}/apply
```
