import pytest


pytestmark = pytest.mark.asyncio


async def test_task_defaults_to_pending_low_without_category_or_tags(
    client,
    auth_headers_factory,
):
    headers, _ = await auth_headers_factory("taskuser")

    response = await client.post(
        "/tasks",
        json={"title": "  Pay invoices  "},
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Pay invoices"
    assert body["status"] == "PENDING"
    assert body["manual_priority"] == "LOW"
    assert body["category_id"] is None
    assert body["tags"] == []


async def test_user_can_create_tag_and_attach_it_to_task(client, auth_headers_factory):
    headers, _ = await auth_headers_factory("taguser")
    task_response = await client.post(
        "/tasks",
        json={"title": "Prepare presentation"},
        headers=headers,
    )
    tag_response = await client.post(
        "/tags",
        json={"name": "  license  "},
        headers=headers,
    )

    response = await client.post(
        f"/tasks/{task_response.json()['id']}/tags/{tag_response.json()['id']}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["tags"] == [
        {
            "id": tag_response.json()["id"],
            "name": "license",
        }
    ]


async def test_user_can_create_task_with_existing_tags(client, auth_headers_factory):
    headers, _ = await auth_headers_factory("taskwithtags")
    tag_response = await client.post(
        "/tags",
        json={"name": "backend"},
        headers=headers,
    )

    response = await client.post(
        "/tasks",
        json={
            "title": "Wire frontend task form",
            "manual_priority": "MEDIUM",
            "tag_ids": [tag_response.json()["id"]],
        },
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["manual_priority"] == "MEDIUM"
    assert response.json()["tags"] == [
        {
            "id": tag_response.json()["id"],
            "name": "backend",
        }
    ]


async def test_users_only_see_their_own_tasks(client, auth_headers_factory):
    first_headers, _ = await auth_headers_factory("firstuser")
    second_headers, _ = await auth_headers_factory("seconduser")

    await client.post("/tasks", json={"title": "First task"}, headers=first_headers)
    await client.post("/tasks", json={"title": "Second task"}, headers=second_headers)

    response = await client.get("/tasks", headers=first_headers)

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["First task"]
