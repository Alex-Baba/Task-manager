import pytest

from app.core.enums import CategoryEnum, PriorityEnum
from app.schemas.task_predictions import PredictionResult


pytestmark = pytest.mark.asyncio


async def test_complete_task_prediction_flow(
    client,
    auth_headers_factory,
    monkeypatch,
):
    def fake_predict_task(task):
        return PredictionResult(
            predicted_priority=PriorityEnum.HIGH,
            predicted_category=CategoryEnum.WORK,
            category_confidence=0.87,
            priority_confidence=0.93,
            smart_score=0.91,
            reasoning={"source": "full-flow-test"},
            model_version="test-model",
        )

    monkeypatch.setattr("app.services.predictions.predict_task", fake_predict_task)
    headers, user = await auth_headers_factory("fullflow")

    me_response = await client.get("/auth/me", headers=headers)
    categories_response = await client.get("/categories")
    tag_response = await client.post(
        "/tags",
        json={"name": "licenta"},
        headers=headers,
    )
    task_response = await client.post(
        "/tasks",
        json={
            "title": "Finalize backend tests",
            "description": "Cover the main user workflow",
        },
        headers=headers,
    )

    task_id = task_response.json()["id"]
    tag_id = tag_response.json()["id"]
    prediction_response = await client.post(
        f"/tasks/{task_id}/predictions/generate",
        headers=headers,
    )
    prediction_id = prediction_response.json()["id"]
    apply_response = await client.post(
        f"/tasks/{task_id}/predictions/{prediction_id}/apply",
        json={"apply_category": True, "apply_priority": True},
        headers=headers,
    )
    attach_tag_response = await client.post(
        f"/tasks/{task_id}/tags/{tag_id}",
        headers=headers,
    )
    complete_response = await client.patch(
        f"/tasks/{task_id}",
        json={"status": "COMPLETED"},
        headers=headers,
    )
    delete_response = await client.delete(f"/tasks/{task_id}", headers=headers)
    deleted_task_response = await client.get(f"/tasks/{task_id}", headers=headers)

    assert me_response.status_code == 200
    assert me_response.json()["id"] == user["id"]
    assert me_response.json()["is_admin"] is False

    assert categories_response.status_code == 200
    assert {category["name"] for category in categories_response.json()} == {
        category.value for category in CategoryEnum
    }

    assert tag_response.status_code == 201
    assert tag_response.json()["name"] == "licenta"

    assert task_response.status_code == 201
    assert task_response.json()["status"] == "PENDING"
    assert task_response.json()["manual_priority"] == "LOW"
    assert task_response.json()["category_id"] is None

    assert prediction_response.status_code == 201
    assert prediction_response.json()["predicted_category"] == "WORK"
    assert prediction_response.json()["predicted_priority"] == "HIGH"

    assert apply_response.status_code == 200
    assert apply_response.json()["manual_priority"] == "HIGH"
    assert apply_response.json()["category_id"] is not None

    assert attach_tag_response.status_code == 200
    assert attach_tag_response.json()["tags"] == [
        {
            "id": tag_id,
            "name": "licenta",
        }
    ]

    assert complete_response.status_code == 200
    assert complete_response.json()["status"] == "COMPLETED"
    assert complete_response.json()["completed_at"] is not None

    assert delete_response.status_code == 200
    assert deleted_task_response.status_code == 404
