"""add cascade to task tags

Revision ID: 4c2f0d3e9a1b
Revises: 8b8b4a2f6d1c
Create Date: 2026-06-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4c2f0d3e9a1b"
down_revision: Union[str, Sequence[str], None] = "8b8b4a2f6d1c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("task_tags_task_id_fkey", "task_tags", type_="foreignkey")
    op.drop_constraint("task_tags_tag_id_fkey", "task_tags", type_="foreignkey")
    op.create_foreign_key(
        "task_tags_task_id_fkey",
        "task_tags",
        "tasks",
        ["task_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "task_tags_tag_id_fkey",
        "task_tags",
        "tags",
        ["tag_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("task_tags_task_id_fkey", "task_tags", type_="foreignkey")
    op.drop_constraint("task_tags_tag_id_fkey", "task_tags", type_="foreignkey")
    op.create_foreign_key(
        "task_tags_task_id_fkey",
        "task_tags",
        "tasks",
        ["task_id"],
        ["id"],
    )
    op.create_foreign_key(
        "task_tags_tag_id_fkey",
        "task_tags",
        "tags",
        ["tag_id"],
        ["id"],
    )
