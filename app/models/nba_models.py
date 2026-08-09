from datetime import UTC, datetime

from marshmallow import fields, post_dump

from app import db, ma


def serialize_utc_timestamp(person):
    """Serialize database timestamps as RFC 3339 UTC values."""
    value = person.timestamp
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()


class Person(db.Model):
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class PersonSchema(ma.SQLAlchemyAutoSchema):
    timestamp = fields.Function(serialize=serialize_utc_timestamp, dump_only=True)

    @post_dump
    def omit_unknown_timestamp(self, data, **_kwargs):
        """Do not emit an invalid date-time for nullable legacy rows."""
        if data.get("timestamp") is None:
            data.pop("timestamp", None)
        return data

    class Meta:
        model = Person
        sqla_session = db.session
        load_instance = True
