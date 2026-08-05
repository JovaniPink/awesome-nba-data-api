"""Database initialization command."""

import click
from flask.cli import with_appcontext

from app import db
from app.models.nba_models import Person


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    init_db()


def init_db():
    """Reset the database and load development sample records."""
    db.drop_all()
    db.create_all()
    create_people()


def create_people():
    """Create sample people records."""
    people = [
        {"fname": "Doug", "lname": "Farrell"},
        {"fname": "Kent", "lname": "Brockman"},
        {"fname": "Bunny", "lname": "Easter"},
    ]

    for person in people:
        db.session.add(Person(lname=person["lname"], fname=person["fname"]))

    db.session.commit()
