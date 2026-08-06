# Tests

Run the test suite from the repository root:

```sh
pytest -q
```

`test_app.py` covers the rendered landing page and the OpenAPI people endpoint
using a temporary SQLite database. It also contains a PostgreSQL integration
test that is skipped unless `TEST_DATABASE_URL` is set with an explicit reason.

CI starts PostgreSQL 18 and uses:

```sh
export TEST_DATABASE_URL=postgresql://nbaapi:test-only@localhost:5432/nbaapi
pytest -q
```

The integration test verifies the server major version, applies the checked-in
Alembic migration, confirms the `person` table exists, and downgrades to the
empty migration base. Use a disposable database only; the test intentionally
changes application tables.
