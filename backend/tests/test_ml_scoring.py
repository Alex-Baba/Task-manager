from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.core.enums import PriorityEnum
from app.ml.scoring import calculate_prediction_score


def make_task(title: str, description: str = "", due_date=None):
    return SimpleNamespace(
        title=title,
        description=description,
        due_date=due_date,
        tags=[],
    )


def test_critical_text_without_due_date_can_still_be_high_priority():
    priority, score, reasoning = calculate_prediction_score(
        task=make_task("critical production outage"),
        category_confidence=0.9,
    )

    assert priority == PriorityEnum.HIGH
    assert score >= 0.68
    assert "critical_urgency_floor_applied" in reasoning["scoring_notes"]


def test_category_confidence_alone_does_not_raise_priority():
    priority, score, reasoning = calculate_prediction_score(
        task=make_task("read article later"),
        category_confidence=0.98,
    )

    assert priority == PriorityEnum.LOW
    assert score < 0.2
    assert reasoning["category_confidence"] == 0.98


def test_urgent_task_due_soon_becomes_high_priority():
    priority, score, reasoning = calculate_prediction_score(
        task=make_task(
            "urgent bug fix",
            due_date=datetime.now(timezone.utc) + timedelta(days=1),
        ),
        category_confidence=0.65,
    )

    assert priority == PriorityEnum.HIGH
    assert score >= 0.68
    assert "deadline_and_urgency_floor_applied" in reasoning["scoring_notes"]


def test_romanian_urgency_is_detected():
    priority, score, reasoning = calculate_prediction_score(
        task=make_task("operatie urgenta", "trebuie sa merg la spital"),
        category_confidence=0.7,
    )

    assert priority == PriorityEnum.MEDIUM
    assert score >= 0.4
    assert "urgenta" in reasoning["urgency"]["matched_keywords"]


def test_due_today_without_urgency_stays_medium_priority():
    priority, score, reasoning = calculate_prediction_score(
        task=make_task(
            "buy groceries",
            due_date=datetime.now(timezone.utc) + timedelta(hours=2),
        ),
        category_confidence=0.7,
    )

    assert priority == PriorityEnum.MEDIUM
    assert score < 0.68
    assert "near_deadline_floor_applied" in reasoning["scoring_notes"]
