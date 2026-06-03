import pytest

from app.core.enums import CategoryEnum, PriorityEnum
from app.schemas.task_predictions import PredictionResult


pytestmark = pytest.mark.asyncio


async def test_user_can_generate_and_apply_prediction(
    client,
    auth_headers_factory,
    monkeypatch,
):
    def fake_predict_task(task):
        return PredictionResult(
            predicted_priority=PriorityEnum.HIGH,
            predicted_category=CategoryEnum.FINANCE,
            category_confidence=0.82,
            priority_confidence=0.91,
            smart_score=0.88,
            reasoning={"source": "test"},
            model_version="test-model",
        )

    monkeypatch.setattr("app.services.predictions.predict_task", fake_predict_task)
    headers, _ = await auth_headers_factory("predictionuser")
    task_response = await client.post(
        "/tasks",
        json={"title": "Pay rent"},
        headers=headers,
    )
    task_id = task_response.json()["id"]

    prediction_response = await client.post(
        f"/tasks/{task_id}/predictions/generate",
        headers=headers,
    )
    prediction = prediction_response.json()
    apply_response = await client.post(
        f"/tasks/{task_id}/predictions/{prediction['id']}/apply",
        json={"apply_category": True, "apply_priority": True},
        headers=headers,
    )
    active_response = await client.get(
        f"/tasks/{task_id}/predictions/active",
        headers=headers,
    )

    assert prediction_response.status_code == 201
    assert prediction["predicted_category"] == "FINANCE"
    assert prediction["predicted_priority"] == "HIGH"
    assert apply_response.status_code == 200
    assert apply_response.json()["manual_priority"] == "HIGH"
    assert apply_response.json()["category_id"] is not None
    assert active_response.status_code == 200
    assert active_response.json()["applied_category"] is True
    assert active_response.json()["applied_priority"] is True
