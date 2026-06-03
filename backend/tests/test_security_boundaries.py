import pytest

from app.core.enums import CategoryEnum, PriorityEnum
from app.schemas.task_predictions import PredictionResult


pytestmark = pytest.mark.asyncio


async def test_user_cannot_access_or_modify_another_users_task(
    client,
    auth_headers_factory,
):
    owner_headers, _ = await auth_headers_factory("taskowner")
    other_headers, _ = await auth_headers_factory("taskintruder")
    task_response = await client.post(
        "/tasks",
        json={"title": "Private task"},
        headers=owner_headers,
    )
    task_id = task_response.json()["id"]

    get_response = await client.get(f"/tasks/{task_id}", headers=other_headers)
    update_response = await client.patch(
        f"/tasks/{task_id}",
        json={"title": "Changed by someone else"},
        headers=other_headers,
    )
    delete_response = await client.delete(f"/tasks/{task_id}", headers=other_headers)
    owner_response = await client.get(f"/tasks/{task_id}", headers=owner_headers)

    assert get_response.status_code == 404
    assert update_response.status_code == 404
    assert delete_response.status_code == 404
    assert owner_response.status_code == 200
    assert owner_response.json()["title"] == "Private task"


async def test_user_cannot_attach_another_users_tag_to_their_task(
    client,
    auth_headers_factory,
):
    owner_headers, _ = await auth_headers_factory("tagowner")
    other_headers, _ = await auth_headers_factory("tagintruder")
    tag_response = await client.post(
        "/tags",
        json={"name": "private"},
        headers=owner_headers,
    )
    task_response = await client.post(
        "/tasks",
        json={"title": "Other user task"},
        headers=other_headers,
    )

    response = await client.post(
        f"/tasks/{task_response.json()['id']}/tags/{tag_response.json()['id']}",
        headers=other_headers,
    )

    assert response.status_code == 404


async def test_user_cannot_read_another_users_predictions(
    client,
    auth_headers_factory,
    monkeypatch,
):
    def fake_predict_task(task):
        return PredictionResult(
            predicted_priority=PriorityEnum.MEDIUM,
            predicted_category=CategoryEnum.EDUCATION,
            category_confidence=0.77,
            priority_confidence=0.62,
            smart_score=0.68,
            reasoning={"source": "security-test"},
            model_version="test-model",
        )

    monkeypatch.setattr("app.services.predictions.predict_task", fake_predict_task)
    owner_headers, _ = await auth_headers_factory("predictionowner")
    other_headers, _ = await auth_headers_factory("predictionintruder")
    task_response = await client.post(
        "/tasks",
        json={"title": "Private prediction task"},
        headers=owner_headers,
    )
    task_id = task_response.json()["id"]
    await client.post(f"/tasks/{task_id}/predictions/generate", headers=owner_headers)

    response = await client.get(f"/tasks/{task_id}/predictions", headers=other_headers)

    assert response.status_code == 404
