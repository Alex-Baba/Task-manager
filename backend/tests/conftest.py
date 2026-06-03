import os
import sys
from collections.abc import AsyncGenerator, Callable
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@pytest_asyncio.fixture
async def session_maker() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    test_database_url = os.getenv("TEST_DATABASE_URL")
    if not test_database_url:
        pytest.skip("Set TEST_DATABASE_URL to run integration tests")

    os.environ["DATABASE_URL"] = test_database_url

    import app.models  # noqa: F401
    from app.core.enums import CategoryEnum
    from app.models.base import Base
    from app.models.categories import Categories

    engine = create_async_engine(test_database_url)
    testing_session_maker = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with testing_session_maker() as session:
        session.add_all(Categories(name=category) for category in CategoryEnum)
        await session.commit()

    try:
        yield testing_session_maker
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture
async def app_instance(session_maker: async_sessionmaker[AsyncSession]):
    from app.db.session import get_session
    from app.main import create_app

    app = create_app()

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    try:
        yield app
    finally:
        app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app_instance) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app_instance)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client


@pytest_asyncio.fixture
async def db_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


@pytest.fixture
def user_payload_factory() -> Callable[[str], dict[str, str]]:
    def make_user(username: str = "testuser") -> dict[str, str]:
        return {
            "username": username,
            "email": f"{username}@example.com",
            "password": "TestPassword123",
        }

    return make_user


@pytest.fixture
def auth_headers_factory(
    client: AsyncClient,
    user_payload_factory: Callable[[str], dict[str, str]],
) -> Callable[[str], Any]:
    async def make_headers(username: str = "testuser"):
        payload = user_payload_factory(username)
        create_response = await client.post("/users", json=payload)
        assert create_response.status_code == 201

        login_response = await client.post(
            "/auth/login",
            data={
                "username": payload["username"],
                "password": payload["password"],
            },
        )
        assert login_response.status_code == 200

        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}, create_response.json()

    return make_headers
