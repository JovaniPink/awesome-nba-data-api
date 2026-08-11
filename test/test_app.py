"""Application and database smoke tests for the supported runtime."""

import os
from pathlib import Path

import pytest
import yaml
from flask_migrate import downgrade, upgrade
from sqlalchemy import inspect, text

from app import create_app, db
from app.models.nba_models import Person


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
    assert response.headers["content-type"] == "application/json"
    assert response.json() == []


def test_people_endpoint_is_stably_ordered_and_bounded(application):
    with application.app.app_context():
        db.session.add_all(
            [
                Person(fname=f"First {index:02d}", lname=f"Last {index % 3}")
                for index in range(60)
            ]
        )
        db.session.commit()

    response = application.test_client().get("/api/people")

    assert response.status_code == 200
    assert len(response.json()) == 50
    ordered_names = [(person["lname"], person["fname"]) for person in response.json()]
    assert ordered_names == sorted(ordered_names)

    final_page = application.test_client().get("/api/people?limit=10&offset=50")
    assert final_page.status_code == 200
    assert len(final_page.json()) == 10


def test_people_endpoint_rejects_invalid_or_unknown_query_parameters(application):
    client = application.test_client()

    responses = [
        client.get("/api/people?limit=0"),
        client.get("/api/people?limit=101"),
        client.get("/api/people?unexpected=true"),
    ]
    assert all(response.status_code == 400 for response in responses)
    assert all(
        response.headers["content-type"] == "application/problem+json"
        for response in responses
    )


def test_person_detail_endpoint_returns_one_or_404(application):
    with application.app.app_context():
        person = Person(fname="Ja", lname="Morant")
        db.session.add(person)
        db.session.commit()
        person_id = person.person_id

    client = application.test_client()
    found = client.get(f"/api/people/{person_id}")
    missing = client.get("/api/people/999999")

    assert found.status_code == 200
    assert found.headers["content-type"] == "application/json"
    assert found.json()["person_id"] == person_id
    assert found.json()["fname"] == "Ja"
    assert found.json()["lname"] == "Morant"
    assert found.json()["timestamp"].endswith("+00:00")
    assert missing.status_code == 404
    assert missing.headers["content-type"] == "application/problem+json"
    assert missing.json()["status"] == 404


def test_openapi_contract_identifies_the_service():
    specification = yaml.safe_load(Path("app/swagger.yaml").read_text(encoding="utf-8"))

    assert specification["openapi"] == "3.0.3"
    assert "swagger" not in specification
    assert specification["info"]["title"] == "NBA Data API"
    assert specification["servers"] == [{"url": "/api"}]
    assert "/people" in specification["paths"]
    assert "/people/{person_id}" in specification["paths"]
    assert (
        specification["paths"]["/people"]["get"]["parameters"][0]["schema"]["maximum"]
        == 100
    )
    assert (
        specification["paths"]["/people"]["get"]["responses"]["200"]["content"][
            "application/json"
        ]["schema"]["items"]["$ref"]
        == "#/components/schemas/Person"
    )
    assert "definitions" not in specification
    for operations in specification["paths"].values():
        assert set(operations).isdisjoint({"post", "put", "patch", "delete"})


def test_legacy_sample_blueprint_remains_available(application):
    response = application.test_client().get("/nbadata")

    assert response.status_code == 200
    assert response.json() == {"sample return": 10}


def test_sqlite_schema_round_trip(tmp_path):
    database_path = tmp_path / "nbaapi-migration-test.db"
    connexion_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
        }
    )

    with connexion_app.app.app_context():
        upgrade()
        assert inspect(db.engine).has_table("person")
        downgrade(revision="base")
        assert not inspect(db.engine).has_table("person")


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
        timestamp_column = next(
            column
            for column in inspect(db.engine).get_columns("person")
            if column["name"] == "timestamp"
        )
        assert timestamp_column["type"].timezone is True
        downgrade(revision="base")
