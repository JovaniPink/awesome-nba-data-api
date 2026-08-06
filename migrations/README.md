# Database migrations

This directory contains the Flask-Migrate/Alembic environment for the database
configured by `SQLALCHEMY_DATABASE_URI`.

Run migration commands through the Flask application context:

```sh
flask --app manage db current
flask --app manage db migrate -m "describe the schema change"
flask --app manage db upgrade
```

Review every generated revision before committing it. Schema migrations and
PostgreSQL major-version upgrades are separate operations: Alembic changes the
application schema, while a PostgreSQL 13-to-18 move requires a verified
database backup/restore or `pg_upgrade` process outside this repository.

`versions/3f45a7d8b2c1_create_person_table.py` is the checked-in schema baseline.
The development-only `flask --app manage init-db` command bypasses migration
history and recreates the schema destructively.

See the [Flask-Migrate documentation](https://flask-migrate.readthedocs.io/)
and [Alembic documentation](https://alembic.sqlalchemy.org/).
