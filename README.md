# NBA Data API

OpenAPI-first NBA data service built with Python 3.14, Connexion 3, Flask 3, SQLAlchemy 2, and
PostgreSQL 18. Uvicorn serves the Connexion ASGI application; Docker Compose adds PostgreSQL and an
Nginx reverse proxy.

This repository currently exposes a small people API and the supporting application/database
baseline. It is not yet the complete NBA statistics platform described by older versions of this
README.

## Architecture

```text
client
  -> nginx :80
    -> uvicorn / Connexion :5000
      -> Flask application factory
        -> OpenAPI operations and Flask blueprints
        -> SQLAlchemy / Alembic
          -> PostgreSQL 18
```

- `app/swagger.yaml` is the authoritative OpenAPI route contract.
- `app/api/` implements OpenAPI `operationId` handlers.
- `app/views/` owns HTML and non-OpenAPI Flask blueprints.
- `app/models/` owns SQLAlchemy models and Marshmallow schemas.
- `migrations/` owns the Alembic schema history.
- `unicorn.py` exposes the Connexion ASGI application consumed by Uvicorn.
- `manage.py` exposes the underlying Flask application for CLI and migration commands.
- `app/celery/` is an unintegrated worker scaffold; Compose does not currently run a broker or
  worker.

## Requirements

- Python 3.14
- Docker Desktop or another Docker Engine with Compose v2-compatible commands
- PostgreSQL is optional for the fast unit gate and required for the integration gate

## Local setup

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --disable-pip-version-check -r requirements-dev.txt
cp .env.example .env
```

`requirements.in` / `requirements.txt` own the production graph copied into the image.
`requirements-dev.in` / `requirements-dev.txt` extend that graph with tests, linting, auditing, and
lockfile tooling. Regenerate both locks on Python 3.14:

```bash
pip-compile --upgrade --output-file=requirements.txt --strip-extras requirements.in
pip-compile --upgrade --output-file=requirements-dev.txt --strip-extras requirements-dev.in
```

Never put production credentials in `.env`; the checked-in example values are local placeholders.

## Run without Docker

The application falls back to a local SQLite database when `DATABASE_URL` is unset:

```bash
flask --app manage db upgrade
uvicorn unicorn:app --host 0.0.0.0 --port 5000
```

Open:

- landing page: http://localhost:5000/
- Swagger UI: http://localhost:5000/api/ui/
- people endpoint: http://localhost:5000/api/people
- legacy sample blueprint: http://localhost:5000/nbadata

`/home` is login-protected, but the repository does not yet define a persistent user model.

## Run the full stack

```bash
cp .env.example .env
docker compose config --quiet
docker compose up --build
```

Compose waits for PostgreSQL and the API health check before starting Nginx. The API container
applies checked-in Alembic migrations before Uvicorn starts. Nginx publishes the stack on
http://localhost:80.

TLS termination, rate limiting, production secrets, backups, and a database major-version migration
procedure are deployment responsibilities outside this repository.

PostgreSQL data lives in the named `postgres_data` volume at `/var/lib/postgresql`. Stop the stack
without deleting that volume:

```bash
docker compose down
```

Do not add `--volumes` unless permanent deletion of local database data is intentional.

### PostgreSQL major-version upgrades

Changing the image tag does not upgrade an existing PostgreSQL data directory in place. Before
moving a database with needed data from PostgreSQL 13 to 18, create and verify a logical backup,
then restore it into a new PostgreSQL 18 volume (or use a separately validated `pg_upgrade`
procedure). Never attach a PostgreSQL 13 data directory directly to PostgreSQL 18. Review the
[official PostgreSQL image storage guidance](https://github.com/docker-library/docs/blob/master/postgres/README.md#pgdata)
before a real migration.

## Database commands

Run schema changes through Flask-Migrate:

```bash
flask --app manage db current
flask --app manage db migrate -m "describe the schema change"
flask --app manage db upgrade
```

Review generated revisions before committing them. `flask --app manage init-db` is a destructive
development command that drops and recreates tables; it is not a migration or production recovery
path. See [`migrations/README.md`](migrations/README.md) for the full boundary.

## Validation

Fast local gate:

```bash
python -m pytest -q
ruff check app manage.py unicorn.py test
python -m openapi_spec_validator app/swagger.yaml
pip-audit -r requirements.txt
docker compose config --quiet
docker build --tag awesome-nba-data-api:test .
```

The PostgreSQL integration test intentionally applies and downgrades the schema, so use a disposable
database only:

```bash
export TEST_DATABASE_URL=postgresql://nbaapi:test-only@localhost:5432/nbaapi
python -m pytest -q
```

CI starts a disposable PostgreSQL 18 service, runs all tests, validates the Compose model, and builds
the production image. The image contains only the runtime lockfile and runs as unprivileged UID
`10001`.

## Contributing

When adding an API route, update `app/swagger.yaml`, implement the referenced `operationId`, and add
a request test. Keep blueprint-only routes documented here and preserve the application-factory
boundary described in [`app/README.md`](app/README.md).

## License

[MIT](LICENSE)
