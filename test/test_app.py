"""Application and database smoke tests for the supported runtime."""

import os

import pytest
from flask_migrate import downgrade, upgrade
from sqlalchemy import inspect, text

from app import create_app, db


@pytest.fixture()
def application(tmp_path):
    database_path = tmp_path / "nbaapi-test.db"
    connexion_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )

    with connexion_app.app.app_context():
        db.create_all()

    return connexion_app


def test_landing_page_renders(application):
    response = application.test_client().get("/")

    assert response.status_code == 200
    assert "NBA data API" in response.text


def test_people_endpoint_uses_openapi_route(application):
    response = application.test_client().get("/api/people")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.integration
def test_postgres_18_schema_round_trip():
    """Prove the ORM can connect to and create its schema on PostgreSQL 18."""
    database_url = os.environ.get("TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("TEST_DATABASE_URL is provided by the PostgreSQL integration gate")

    connexion_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": database_url,
        }
    )

    with connexion_app.app.app_context():
        version_number = db.session.execute(
            text("SELECT current_setting('server_version_num')::integer")
        ).scalar_one()
        assert version_number >= 180000
        db.session.rollback()

        upgrade()
        assert inspect(db.engine).has_table("person")
        downgrade(revision="base")
