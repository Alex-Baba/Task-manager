"""unify category and priority enums

Revision ID: c7d8e9f0a1b2
Revises: b1d2c3e4f5a6, 4c2f0d3e9a1b
Create Date: 2026-06-03 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c7d8e9f0a1b2"
down_revision: Union[str, Sequence[str], None] = (
    "b1d2c3e4f5a6",
    "4c2f0d3e9a1b",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    category_enum = sa.Enum(
        "WORK",
        "PERSONAL",
        "SHOPPING",
        "HEALTH",
        "FINANCE",
        "EDUCATION",
        "ENTERTAINMENT",
        "OTHER",
        name="category",
    )
    priority_enum = sa.Enum("LOW", "MEDIUM", "HIGH", name="priority")

    category_enum.create(op.get_bind(), checkfirst=True)
    priority_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "task_predictions",
        "predicted_category",
        existing_type=sa.Enum(
            "WORK",
            "PERSONAL",
            "SHOPPING",
            "HEALTH",
            "FINANCE",
            "EDUCATION",
            "ENTERTAINMENT",
            "OTHER",
            name="categoryenum",
        ),
        type_=category_enum,
        existing_nullable=False,
        postgresql_using="predicted_category::text::category",
    )
    op.alter_column(
        "task_predictions",
        "predicted_priority",
        existing_type=sa.Enum("LOW", "MEDIUM", "HIGH", name="priorityenum"),
        type_=priority_enum,
        existing_nullable=False,
        postgresql_using="predicted_priority::text::priority",
    )

    sa.Enum(name="categoryenum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="priorityenum").drop(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    old_category_enum = sa.Enum(
        "WORK",
        "PERSONAL",
        "SHOPPING",
        "HEALTH",
        "FINANCE",
        "EDUCATION",
        "ENTERTAINMENT",
        "OTHER",
        name="categoryenum",
    )
    old_priority_enum = sa.Enum("LOW", "MEDIUM", "HIGH", name="priorityenum")

    old_category_enum.create(op.get_bind(), checkfirst=True)
    old_priority_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "task_predictions",
        "predicted_category",
        existing_type=sa.Enum(
            "WORK",
            "PERSONAL",
            "SHOPPING",
            "HEALTH",
            "FINANCE",
            "EDUCATION",
            "ENTERTAINMENT",
            "OTHER",
            name="category",
        ),
        type_=old_category_enum,
        existing_nullable=False,
        postgresql_using="predicted_category::text::categoryenum",
    )
    op.alter_column(
        "task_predictions",
        "predicted_priority",
        existing_type=sa.Enum("LOW", "MEDIUM", "HIGH", name="priority"),
        type_=old_priority_enum,
        existing_nullable=False,
        postgresql_using="predicted_priority::text::priorityenum",
    )
