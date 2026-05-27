from app.models.task_predictions import PriorityEnum
from app.ml.keyword_rules import calculate_urgency_score
from app.ml.utils import calculate_days_until_due


def calculate_deadline_score(due_date) -> float:
    days = calculate_days_until_due(due_date)

    if days is None:
        return 0.0

    if days < 0:
        return 1.0

    if days == 0:
        return 0.9

    if days <= 2:
        return 0.75

    if days <= 7:
        return 0.45

    return 0.1


def priority_from_score(score: float) -> PriorityEnum:
    if score >= 0.7:
        return PriorityEnum.HIGH

    if score >= 0.4:
        return PriorityEnum.MEDIUM

    return PriorityEnum.LOW


def calculate_prediction_score(
    task,
    category_confidence: float,
) -> tuple[PriorityEnum, float, dict]:
    text = f"{task.title or ''} {task.description or ''}"

    urgency = calculate_urgency_score(text)
    deadline_score = calculate_deadline_score(task.due_date)

    smart_score = (
        deadline_score * 0.45
        + urgency["score"] * 0.35
        + category_confidence * 0.20
    )

    smart_score = round(min(max(smart_score, 0.0), 1.0), 3)

    predicted_priority = priority_from_score(smart_score)

    reasoning = {
        "deadline_score": deadline_score,
        "urgency": urgency,
        "category_confidence": category_confidence,
        "weights": {
            "deadline_score": 0.45,
            "urgency_score": 0.35,
            "category_confidence": 0.20,
        },
        "explanation": "Priority calculated from deadline proximity, urgency keywords and ML category confidence.",
    }

    return predicted_priority, smart_score, reasoning