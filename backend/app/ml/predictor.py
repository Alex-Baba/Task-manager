from app.core.enums import CategoryEnum
from app.ml.model_loader import get_category_model
from app.ml.builder import build_category_text
from app.ml.scoring import calculate_prediction_score
from app.schemas.task_predictions import PredictionResult


MODEL_VERSION = "task_category_model_datasetv6"
MIN_CATEGORY_CONFIDENCE = 0.30
MIN_CATEGORY_MARGIN = 0.05


def resolve_category_prediction(
    classes,
    probabilities,
) -> tuple[CategoryEnum, float, dict]:
    ranked_predictions = sorted(
        (
            (
                category
                if isinstance(category, CategoryEnum)
                else CategoryEnum(str(category)),
                float(probability),
            )
            for category, probability in zip(classes, probabilities)
        ),
        key=lambda prediction: prediction[1],
        reverse=True,
    )
    top_category, top_confidence = ranked_predictions[0]
    second_prediction = ranked_predictions[1] if len(ranked_predictions) > 1 else None
    margin = (
        top_confidence - second_prediction[1] if second_prediction is not None else None
    )
    fallback_reason = None

    if top_confidence < MIN_CATEGORY_CONFIDENCE:
        fallback_reason = "low_confidence"
    elif margin is not None and margin < MIN_CATEGORY_MARGIN:
        fallback_reason = "low_margin"

    final_category = CategoryEnum.OTHER if fallback_reason else top_category

    reasoning = {
        "final_category": final_category.value,
        "original_predicted_category": top_category.value,
        "top_confidence": round(top_confidence, 3),
        "second_category": second_prediction[0].value if second_prediction else None,
        "second_confidence": (
            round(second_prediction[1], 3) if second_prediction else None
        ),
        "margin": round(margin, 3) if margin is not None else None,
        "fallback_applied": fallback_reason is not None,
        "fallback_reason": fallback_reason,
        "thresholds": {
            "min_confidence": MIN_CATEGORY_CONFIDENCE,
            "min_margin": MIN_CATEGORY_MARGIN,
        },
    }

    return final_category, top_confidence, reasoning


def predict_task(task) -> PredictionResult:
    model = get_category_model()

    text = build_category_text(task)

    probabilities = model.predict_proba([text])[0]
    predicted_category, category_confidence, category_reasoning = (
        resolve_category_prediction(model.classes_, probabilities)
    )

    predicted_priority, smart_score, reasoning = calculate_prediction_score(
        task=task,
        category_confidence=category_confidence,
    )
    reasoning["category_prediction"] = category_reasoning

    return PredictionResult(
        predicted_category=predicted_category,
        category_confidence=category_confidence,
        predicted_priority=predicted_priority,
        priority_confidence=smart_score,
        smart_score=smart_score,
        reasoning=reasoning,
        model_version=MODEL_VERSION,
    )
