# NBA API

A small Connexion and Flask service that exposes an OpenAPI-defined people
endpoint and provides a foundation for NBA data experiments used by
Measured Studios.

## Current API surface

| Route | Purpose |
| --- | --- |
| `GET /` | Render the landing page. |
| `GET /api/people` | Return people from the database through the OpenAPI handler. |
| `GET /nbadata` | Return the current sample JSON response. |

The OpenAPI contract is in [`app/swagger.yaml`](./app/swagger.yaml). Routes from
the older README that are not present in that file or the Flask blueprints are
not supported by the current code.

## Runtime

- Python 3.14
- Connexion 3 and Flask 3
- SQLAlchemy 2 and Alembic/Flask-Migrate
- PostgreSQL 18 in Docker Compose; SQLite for dependency-free local development
- Uvicorn as the container process
- Nginx as the Compose reverse proxy

Direct and transitive Python dependencies are locked in
[`requirements.txt`](./requirements.txt). Edit [`requirements.in`](./requirements.in)
and regenerate the lock rather than hand-editing transitive pins. Renovate uses
the same `pip-compile` contract and does not update transitive pins independently.

## Local development

Create an isolated Python environment and install the locked dependencies:

```sh
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The application uses `nbaapi.db` in the repository directory when
`DATABASE_URL` is not set. Apply the checked-in migration and start the service:

```sh
flask --app manage:app db upgrade
python manage.py
```

Open <http://localhost:5000/>. For local demo data, `flask --app manage init-db`
drops the configured schema before recreating it and loading sample people.
Never run that destructive command against a database whose contents must be
preserved.

## Docker Compose

Create local configuration, replace every `change-me` value, and start the
stack:

```sh
cp .env.example .env
docker compose up --build
```

The public entry point is <http://localhost/>. Compose waits for PostgreSQL to
accept connections before starting the API and waits for the API health check
before starting Nginx. The API container applies checked-in Alembic migrations
before starting Uvicorn.

PostgreSQL data is stored in the named `postgres_data` volume at the PostgreSQL
18 image's supported `/var/lib/postgresql` mount point. Stop containers without
deleting that volume:

```sh
docker compose down
```

Do not add `--volumes` unless permanently deleting local database data is the
intended action.

### PostgreSQL 13 to 18 upgrade boundary

PostgreSQL major versions do not perform an in-place upgrade merely because the
container image tag changed. Make and verify a logical backup from PostgreSQL 13
before switching a database that contains needed data, then restore it into a
new PostgreSQL 18 volume. Do not attach a PostgreSQL 13 data directory directly
to PostgreSQL 18.

The official image changed its `PGDATA` and volume layout for PostgreSQL 18, so
the Compose volume intentionally targets `/var/lib/postgresql`. Review the
[official image's PostgreSQL 18 storage guidance](https://github.com/docker-library/docs/blob/master/postgres/README.md#pgdata)
before migrating existing data.

## Validation

```sh
python -m pytest -q
cp .env.example .env
docker compose config --quiet
docker build --tag awesome-nba-data-api:test .
```

The normal local test run uses SQLite and explicitly skips the PostgreSQL
integration test. CI provides a PostgreSQL 18 service through
`TEST_DATABASE_URL`; the integration test checks the server major version and
round-trips the checked-in Alembic migration.

The CI workflow also validates the Compose configuration and builds the
production image. The image runs as unprivileged UID `10001`.

## Dependency updates

Regenerate the Python lock with Python 3.14:

```sh
python -m pip install pip-tools
pip-compile --upgrade --resolver=backtracking --strip-extras \
  --output-file=requirements.txt requirements.in
python -m pytest -q
```

Database and container-image upgrades require the Docker and integration gates;
a successful Python unit test alone is not enough.

## Project structure

```text
app/                 Application factory, OpenAPI contract, models, and views
migrations/          Flask-Migrate configuration and checked-in revisions
nginx/               Reverse-proxy configuration for the Compose service
test/                SQLite smoke tests and PostgreSQL integration test
Dockerfile           Non-root Python 3.14 production image
docker-compose.yml   PostgreSQL, API, and Nginx runtime graph
```

## Known limits

- The current OpenAPI contract exposes only the people collection.
- The `nbadata` endpoint is a placeholder and does not yet return NBA data.
- Authentication is scaffolded, but no persistent user loader is implemented.
- There is no production backup or restore automation in this repository.

## Contributing

Keep changes focused, update the OpenAPI contract with handler changes, and run
the relevant unit, PostgreSQL, Compose, and image-build gates before requesting
review.

## License

[MIT](./LICENSE)
