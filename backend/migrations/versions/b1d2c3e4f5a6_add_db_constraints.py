"""add db constraints

Revision ID: b1d2c3e4f5a6
Revises: 9f3a2c1d7e4b
Create Date: 2026-06-02 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1d2c3e4f5a6"
down_revision: Union[str, Sequence[str], None] = "9f3a2c1d7e4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE task_predictions
        SET category_confidence = LEAST(GREATEST(category_confidence, 0), 1),
            priority_confidence = LEAST(GREATEST(priority_confidence, 0), 1),
            smart_score = LEAST(GREATEST(smart_score, 0), 1)
        """
    )
    op.execute(
        """
        UPDATE task_predictions
        SET is_active = false
        WHERE is_active = true
          AND id NOT IN (
              SELECT DISTINCT ON (task_id) id
              FROM task_predictions
              WHERE is_active = true
              ORDER BY task_id, created_at DESC, id DESC
          )
        """
    )
    op.execute(
        """
        UPDATE tasks
        SET title = 'Untitled task'
        WHERE length(trim(title)) = 0
        """
    )
    op.execute(
        """
        UPDATE tasks
        SET completed_at = updated_at
        WHERE status::text = 'COMPLETED'
          AND completed_at IS NULL
        """
    )
    op.execute(
        """
        UPDATE tasks
        SET completed_at = NULL
        WHERE status::text <> 'COMPLETED'
        """
    )
    op.execute(
        """
        UPDATE tags
        SET name = 'untagged-' || substring(id::text, 1, 8)
        WHERE length(trim(name)) = 0
        """
    )

    op.create_check_constraint(
        "ck_task_predictions_category_confidence_range",
        "task_predictions",
        "category_confidence >= 0 AND category_confidence <= 1",
    )
    op.create_check_constraint(
        "ck_task_predictions_priority_confidence_range",
        "task_predictions",
        "priority_confidence >= 0 AND priority_confidence <= 1",
    )
    op.create_check_constraint(
        "ck_task_predictions_smart_score_range",
        "task_predictions",
        "smart_score >= 0 AND smart_score <= 1",
    )
    op.create_index(
        "uq_active_prediction_per_task",
        "task_predictions",
        ["task_id"],
        unique=True,
        postgresql_where=sa.text("is_active = true"),
    )
    op.create_check_constraint(
        "ck_tasks_title_not_empty",
        "tasks",
        "length(trim(title)) > 0",
    )
    op.create_check_constraint(
        "ck_tasks_completed_at_matches_status",
        "tasks",
        """
        (
            status::text = 'COMPLETED'
            AND completed_at IS NOT NULL
        )
        OR
        (
            status::text <> 'COMPLETED'
            AND completed_at IS NULL
        )
        """,
    )
    op.create_check_constraint(
        "ck_tags_name_not_empty",
        "tags",
        "length(trim(name)) > 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_tags_name_not_empty", "tags", type_="check")
    op.drop_constraint("ck_tasks_completed_at_matches_status", "tasks", type_="check")
    op.drop_constraint("ck_tasks_title_not_empty", "tasks", type_="check")
    op.drop_index("uq_active_prediction_per_task", table_name="task_predictions")
    op.drop_constraint(
        "ck_task_predictions_smart_score_range",
        "task_predictions",
        type_="check",
    )
    op.drop_constraint(
        "ck_task_predictions_priority_confidence_range",
        "task_predictions",
        type_="check",
    )
    op.drop_constraint(
        "ck_task_predictions_category_confidence_range",
        "task_predictions",
        type_="check",
    )
