from app.core.enums import PriorityEnum
from app.ml.keyword_rules import calculate_urgency_score
from app.ml.utils import calculate_days_until_due


DEADLINE_WEIGHT = 0.45
URGENCY_WEIGHT = 0.35
CATEGORY_CONFIDENCE_WEIGHT = 0.20

HIGH_PRIORITY_THRESHOLD = 0.7
MEDIUM_PRIORITY_THRESHOLD = 0.4


def clamp_score(score: float) -> float:
    return min(max(score, 0.0), 1.0)


def build_priority_text(task) -> str:
    parts = [
        task.title or "",
        task.description or "",
    ]

    if task.tags:
        parts.extend(tag.name for tag in task.tags)

    return " ".join(parts).strip()


def calculate_deadline_score(due_date) -> tuple[float, str]:
    days = calculate_days_until_due(due_date)

    if days is None:
        return 0.0, "no_due_date"

    if days < 0:
        return 1.0, "overdue"

    if days == 0:
        return 0.9, "today"

    if days <= 2:
        return 0.75, "within_2_days"

    if days <= 7:
        return 0.45, "within_7_days"

    return 0.1, "later"


def priority_from_score(score: float) -> PriorityEnum:
    if score >= HIGH_PRIORITY_THRESHOLD:
        return PriorityEnum.HIGH

    if score >= MEDIUM_PRIORITY_THRESHOLD:
        return PriorityEnum.MEDIUM

    return PriorityEnum.LOW


def calculate_prediction_score(
    task,
    category_confidence: float,
) -> tuple[PriorityEnum, float, dict]:
    category_confidence = clamp_score(category_confidence)
    text = build_priority_text(task)

    urgency = calculate_urgency_score(text)
    deadline_score, deadline_bucket = calculate_deadline_score(task.due_date)

    smart_score = (
        deadline_score * DEADLINE_WEIGHT
        + urgency["score"] * URGENCY_WEIGHT
        + category_confidence * CATEGORY_CONFIDENCE_WEIGHT
    )

    smart_score = round(clamp_score(smart_score), 3)

    predicted_priority = priority_from_score(smart_score)

    reasoning = {
        "deadline_score": deadline_score,
        "deadline_bucket": deadline_bucket,
        "urgency": urgency,
        "category_confidence": category_confidence,
        "weights": {
            "deadline_score": DEADLINE_WEIGHT,
            "urgency_score": URGENCY_WEIGHT,
            "category_confidence": CATEGORY_CONFIDENCE_WEIGHT,
        },
        "thresholds": {
            "medium": MEDIUM_PRIORITY_THRESHOLD,
            "high": HIGH_PRIORITY_THRESHOLD,
        },
        "formula": (
            "deadline_score * 0.45 + urgency_score * 0.35 + category_confidence * 0.20"
        ),
        "explanation": "Priority calculated from deadline proximity, urgency keywords and ML category confidence.",
    }

    return predicted_priority, smart_score, reasoning
