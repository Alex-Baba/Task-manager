import pytest


pytestmark = pytest.mark.asyncio


async def test_user_can_register_login_and_read_current_profile(
    client,
    auth_headers_factory,
):
    headers, user = await auth_headers_factory("alice")

    assert user["username"] == "alice"
    assert "password" not in user

    response = await client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == user["id"]
    assert body["email"] == "alice@example.com"
    assert body["is_admin"] is False


async def test_rejects_password_longer_than_bcrypt_limit(client, user_payload_factory):
    payload = user_payload_factory("longpass")
    payload["password"] = "a" * 73

    response = await client.post("/users", json=payload)

    assert response.status_code == 422
