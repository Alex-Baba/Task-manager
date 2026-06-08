from app.core.enums import PriorityEnum
from app.ml.keyword_rules import calculate_urgency_score
from app.ml.utils import calculate_days_until_due


DEADLINE_WEIGHT = 0.40
URGENCY_WEIGHT = 0.50
CATEGORY_CONFIDENCE_WEIGHT = 0.10

HIGH_PRIORITY_THRESHOLD = 0.68
MEDIUM_PRIORITY_THRESHOLD = 0.4
CRITICAL_URGENCY_THRESHOLD = 0.85
STRONG_URGENCY_THRESHOLD = 0.7


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

    scoring_notes = []

    if urgency["score"] >= CRITICAL_URGENCY_THRESHOLD:
        smart_score = max(smart_score, HIGH_PRIORITY_THRESHOLD + 0.04)
        scoring_notes.append("critical_urgency_floor_applied")

    if deadline_bucket in {"overdue", "today"}:
        smart_score = max(smart_score, MEDIUM_PRIORITY_THRESHOLD + 0.18)
        scoring_notes.append("near_deadline_floor_applied")

    if deadline_bucket in {"overdue", "today", "within_2_days"} and (
        urgency["score"] >= STRONG_URGENCY_THRESHOLD
    ):
        smart_score = max(smart_score, HIGH_PRIORITY_THRESHOLD + 0.04)
        scoring_notes.append("deadline_and_urgency_floor_applied")

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
        "scoring_notes": scoring_notes,
        "thresholds": {
            "medium": MEDIUM_PRIORITY_THRESHOLD,
            "high": HIGH_PRIORITY_THRESHOLD,
        },
        "formula": (
            "deadline_score * 0.40 + urgency_score * 0.50 + category_confidence * 0.10, with floors for critical urgency and near deadlines"
        ),
        "explanation": "Priority calculated mostly from deadline proximity and urgency signals, with category confidence used only as a small support signal.",
    }

    return predicted_priority, smart_score, reasoning
