"""Read-only OpenAPI operations for people data."""

from flask import abort

from app import db
from app.models.nba_models import Person, PersonSchema

JSON_RESPONSE_HEADERS = {"Content-Type": "application/json"}


def read_all(limit=50, offset=0):
    """Return a stable, bounded page of people."""
    statement = (
        db.select(Person)
        .order_by(Person.lname, Person.fname, Person.person_id)
        .limit(limit)
        .offset(offset)
    )
    people = db.session.scalars(statement).all()
    return PersonSchema(many=True).dump(people), 200, JSON_RESPONSE_HEADERS


def read_one(person_id):
    """Return one person or an explicit 404 problem response."""
    person = db.session.get(Person, person_id)
    if person is None:
        abort(404, description=f"Person not found for Id: {person_id}")

    return PersonSchema().dump(person), 200, JSON_RESPONSE_HEADERS
