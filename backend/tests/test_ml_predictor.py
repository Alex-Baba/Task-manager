from app.core.enums import CategoryEnum
from app.ml.predictor import resolve_category_prediction


def test_category_falls_back_to_other_when_confidence_is_low():
    category, confidence, reasoning = resolve_category_prediction(
        [CategoryEnum.WORK, CategoryEnum.PERSONAL, CategoryEnum.HEALTH],
        [0.29, 0.2, 0.18],
    )

    assert category == CategoryEnum.OTHER
    assert confidence == 0.29
    assert reasoning["fallback_applied"] is True
    assert reasoning["fallback_reason"] == "low_confidence"
    assert reasoning["original_predicted_category"] == "WORK"


def test_category_falls_back_to_other_when_margin_is_too_small():
    category, confidence, reasoning = resolve_category_prediction(
        [CategoryEnum.WORK, CategoryEnum.PERSONAL, CategoryEnum.HEALTH],
        [0.41, 0.38, 0.11],
    )

    assert category == CategoryEnum.OTHER
    assert confidence == 0.41
    assert reasoning["fallback_applied"] is True
    assert reasoning["fallback_reason"] == "low_margin"
    assert reasoning["second_category"] == "PERSONAL"
    assert reasoning["margin"] == 0.03


def test_category_is_kept_when_confidence_and_margin_are_clear():
    category, confidence, reasoning = resolve_category_prediction(
        [CategoryEnum.WORK, CategoryEnum.PERSONAL, CategoryEnum.HEALTH],
        [0.42, 0.35, 0.23],
    )

    assert category == CategoryEnum.WORK
    assert confidence == 0.42
    assert reasoning["fallback_applied"] is False
    assert reasoning["fallback_reason"] is None
