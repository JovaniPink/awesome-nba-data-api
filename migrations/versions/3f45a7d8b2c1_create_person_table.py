"""Create the initial person table.

Revision ID: 3f45a7d8b2c1
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision = "3f45a7d8b2c1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "person",
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.Column("lname", sa.String(length=32), nullable=True),
        sa.Column("fname", sa.String(length=32), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("person_id"),
    )


def downgrade():
    op.drop_table("person")
