import pytest

from app.core.enums import CategoryEnum, PriorityEnum
from app.schemas.task_predictions import PredictionResult


pytestmark = pytest.mark.asyncio


async def test_rejects_blank_task_title(client, auth_headers_factory):
    headers, _ = await auth_headers_factory("blanktask")

    response = await client.post(
        "/tasks",
        json={"title": "   "},
        headers=headers,
    )

    assert response.status_code == 422


async def test_rejects_blank_tag_name(client, auth_headers_factory):
    headers, _ = await auth_headers_factory("blanktag")

    response = await client.post(
        "/tags",
        json={"name": "   "},
        headers=headers,
    )

    assert response.status_code == 422


async def test_rejects_prediction_apply_without_selected_fields(
    client,
    auth_headers_factory,
    monkeypatch,
):
    def fake_predict_task(task):
        return PredictionResult(
            predicted_priority=PriorityEnum.LOW,
            predicted_category=CategoryEnum.OTHER,
            category_confidence=0.51,
            priority_confidence=0.49,
            smart_score=0.5,
            reasoning={"source": "validation-test"},
            model_version="test-model",
        )

    monkeypatch.setattr("app.services.predictions.predict_task", fake_predict_task)
    headers, _ = await auth_headers_factory("applynothing")
    task_response = await client.post(
        "/tasks",
        json={"title": "Check apply validation"},
        headers=headers,
    )
    task_id = task_response.json()["id"]
    prediction_response = await client.post(
        f"/tasks/{task_id}/predictions/generate",
        headers=headers,
    )
    prediction_id = prediction_response.json()["id"]

    response = await client.post(
        f"/tasks/{task_id}/predictions/{prediction_id}/apply",
        json={"apply_category": False, "apply_priority": False},
        headers=headers,
    )

    assert response.status_code == 400
