"""Application smoke tests for the supported container runtime."""

import pytest

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
