"""add prediction applied fields

Revision ID: 9f3a2c1d7e4b
Revises: 4c2f0d3e9a1b
Create Date: 2026-06-02 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f3a2c1d7e4b"
down_revision: Union[str, Sequence[str], None] = "4c2f0d3e9a1b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "task_predictions",
        sa.Column(
            "applied_category",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )
    op.add_column(
        "task_predictions",
        sa.Column(
            "applied_priority",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )
    op.add_column(
        "task_predictions",
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.alter_column("task_predictions", "applied_category", server_default=None)
    op.alter_column("task_predictions", "applied_priority", server_default=None)


def downgrade() -> None:
    op.drop_column("task_predictions", "applied_at")
    op.drop_column("task_predictions", "applied_priority")
    op.drop_column("task_predictions", "applied_category")
