"""Store person timestamps with an explicit UTC-aware type.

Revision ID: 5b8f2a4d91c0
Revises: 3f45a7d8b2c1
"""

import sqlalchemy as sa
from alembic import op

revision = "5b8f2a4d91c0"
down_revision = "3f45a7d8b2c1"
branch_labels = None
depends_on = None


def upgrade():
    if op.get_bind().dialect.name != "postgresql":
        return
    op.alter_column(
        "person",
        "timestamp",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
        postgresql_using="timestamp AT TIME ZONE 'UTC'",
    )


def downgrade():
    if op.get_bind().dialect.name != "postgresql":
        return
    op.alter_column(
        "person",
        "timestamp",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=True,
        postgresql_using="timestamp AT TIME ZONE 'UTC'",
    )
