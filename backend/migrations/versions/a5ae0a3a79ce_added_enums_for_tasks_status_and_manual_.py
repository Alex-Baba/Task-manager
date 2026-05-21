"""added enums for tasks status and manual_priority

Revision ID: a5ae0a3a79ce
Revises: 177bfcda0c0b
Create Date: 2026-05-21 14:53:05.538845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5ae0a3a79ce'
down_revision: Union[str, Sequence[str], None] = '177bfcda0c0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    priority_enum = sa.Enum("LOW", "MEDIUM", "HIGH", name="priority")
    status_enum = sa.Enum(
        "PENDING",
        "IN_PROGRESS",
        "COMPLETED",
        "CANCELLED",
        name="status",
    )

    priority_enum.create(op.get_bind(), checkfirst=True)
    status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "tasks",
        sa.Column(
            "manual_priority",
            priority_enum,
            nullable=False,
            server_default="LOW",
        ),
    )

    op.alter_column(
        "tasks",
        "status",
        existing_type=sa.VARCHAR(length=50),
        type_=status_enum,
        existing_nullable=False,
        postgresql_using="status::status",
    )

    op.alter_column("tasks", "manual_priority", server_default=None)


def downgrade() -> None:
    priority_enum = sa.Enum("LOW", "MEDIUM", "HIGH", name="priority")
    status_enum = sa.Enum(
        "PENDING",
        "IN_PROGRESS",
        "COMPLETED",
        "CANCELLED",
        name="status",
    )

    op.alter_column(
        "tasks",
        "status",
        existing_type=status_enum,
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
        postgresql_using="status::varchar",
    )

    op.drop_column("tasks", "manual_priority")

    priority_enum.drop(op.get_bind(), checkfirst=True)
    status_enum.drop(op.get_bind(), checkfirst=True)
