from app.ml.model_loader import get_category_model
from app.ml.builder import build_category_text
from app.ml.scoring import calculate_prediction_score
from app.schemas.task_predictions import PredictionResult


MODEL_VERSION = "task_category_model_datasetv6"


def predict_task(task) -> PredictionResult:
    model = get_category_model()

    text = build_category_text(task)

    predicted_category = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    category_confidence = float(max(probabilities))

    predicted_priority, smart_score, reasoning = calculate_prediction_score(
        task=task,
        category_confidence=category_confidence,
    )

    return PredictionResult(
        predicted_category=predicted_category,
        category_confidence=category_confidence,
        predicted_priority=predicted_priority,
        priority_confidence=smart_score,
        smart_score=smart_score,
        reasoning=reasoning,
        model_version=MODEL_VERSION,
    )