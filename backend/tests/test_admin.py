from uuid import UUID

import pytest

from app.models.admins import Admin


pytestmark = pytest.mark.asyncio


async def test_regular_user_cannot_access_admin_routes(client, auth_headers_factory):
    headers, _ = await auth_headers_factory("regular")

    response = await client.get("/admin/users", headers=headers)

    assert response.status_code == 403


async def test_admin_can_list_users(client, db_session, auth_headers_factory):
    headers, user = await auth_headers_factory("adminuser")
    db_session.add(Admin(user_id=UUID(user["id"])))
    await db_session.commit()

    response = await client.get("/admin/users", headers=headers)

    assert response.status_code == 200
    assert response.json()[0]["id"] == user["id"]


async def test_category_creation_is_admin_only(client, auth_headers_factory):
    headers, _ = await auth_headers_factory("categoryuser")

    response = await client.post(
        "/admin/categories", json={"name": "WORK"}, headers=headers
    )

    assert response.status_code == 403


async def test_admin_can_grant_and_revoke_admin_role(
    client,
    db_session,
    auth_headers_factory,
):
    admin_headers, admin_user = await auth_headers_factory("roleadmin")
    target_headers, target_user = await auth_headers_factory("roletarget")
    db_session.add(Admin(user_id=UUID(admin_user["id"])))
    await db_session.commit()

    grant_response = await client.post(
        f"/admin/users/{target_user['id']}/admin",
        headers=admin_headers,
    )
    me_after_grant_response = await client.get("/auth/me", headers=target_headers)
    revoke_response = await client.delete(
        f"/admin/users/{target_user['id']}/admin",
        headers=admin_headers,
    )
    me_after_revoke_response = await client.get("/auth/me", headers=target_headers)

    assert grant_response.status_code == 201
    assert me_after_grant_response.status_code == 200
    assert me_after_grant_response.json()["is_admin"] is True
    assert revoke_response.status_code == 200
    assert me_after_revoke_response.status_code == 200
    assert me_after_revoke_response.json()["is_admin"] is False
