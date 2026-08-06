# Application package

This directory owns the Connexion application factory and the underlying Flask
application.

## Layout

| Path | Responsibility |
| --- | --- |
| `api/` | Handlers referenced by `swagger.yaml` operation IDs. |
| `commands/` | Flask CLI commands, including the destructive `init-db`. |
| `models/` | SQLAlchemy models and Marshmallow schemas. |
| `static/` | Browser assets served by Flask. |
| `templates/` | Jinja templates for HTML routes. |
| `views/` | Flask blueprints outside the OpenAPI contract. |
| `settings.py` | Environment-backed Flask and database settings. |
| `swagger.yaml` | Authoritative OpenAPI route contract. |

`create_app()` in `app/__init__.py` returns a `connexion.FlaskApp`. Use
`connexion_app.app` when an API requires the underlying Flask object. Extensions
are created once at module level and initialized inside the factory so tests can
construct isolated applications.

When adding an API route, update `swagger.yaml`, implement its `operationId`, and
add a request test. Blueprint-only routes should be registered in
`create_app()` and documented in the root README.
