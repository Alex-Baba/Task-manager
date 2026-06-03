import pytest

from app.core.enums import CategoryEnum


pytestmark = pytest.mark.asyncio


async def test_seeded_categories_are_public(client):
    response = await client.get("/categories")

    assert response.status_code == 200
    names = {category["name"] for category in response.json()}
    assert names == {category.value for category in CategoryEnum}
