# Tests

Run the test suite from the repository root:

```sh
pytest -q
```

`test_app.py` covers the rendered landing page and the OpenAPI people collection
and detail endpoints using a temporary SQLite database. The API cases pin stable
ordering, the default and maximum page boundary, strict rejection of invalid or
unknown query parameters, the OpenAPI 3.0.3 contract shape, explicit success and
problem media types, and the not-found problem response. The module also
contains a PostgreSQL integration test that is skipped unless `TEST_DATABASE_URL`
is set with an explicit reason.

The SQLite gate also applies every checked-in migration and downgrades to the
empty base. PostgreSQL CI additionally verifies that the timestamp column is a
timezone-aware database type.

CI starts PostgreSQL 18 and uses:

```sh
export TEST_DATABASE_URL=postgresql://nbaapi:test-only@localhost:5432/nbaapi
pytest -q
```

The integration test verifies the server major version, applies the checked-in
Alembic migration, confirms the `person` table exists, and downgrades to the
empty migration base. Use a disposable database only; the test intentionally
changes application tables.
