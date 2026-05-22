from app.models.task_predictions import PriorityEnum
from app.ml.keyword_rules import calculate_keyword_score
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


def calculate_prediction_score(task, category_confidence: float):
    text = f"{task.title or ''} {task.description or ''}"

    deadline_score = calculate_deadline_score(task.due_date)
    keyword_score, matched_keywords = calculate_keyword_score(text)

    smart_score = (
        deadline_score * 0.45
        + keyword_score * 0.35
        + category_confidence * 0.20
    )

    smart_score = min(max(smart_score, 0.0), 1.0)

    predicted_priority = priority_from_score(smart_score)

    reasoning = {
        "deadline_score": deadline_score,
        "keyword_score": keyword_score,
        "matched_keywords": matched_keywords,
        "category_confidence": category_confidence,
        "explanation": "Priority calculated from deadline proximity, urgency keywords and ML confidence.",
    }

    return predicted_priority, smart_score, reasoning