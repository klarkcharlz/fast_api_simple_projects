import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.database import Base, get_session

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


async def get_access_token(client, username="testuser", password="testpass"):
    response = client.post("/auth/login/", json={"username": username, "password": password})
    return response.json()["access_token"]


@pytest.fixture(scope="session")
async def test_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="module")
async def override_get_session(test_db):
    async def _override_get_session():
        async with test_db() as session:
            yield session

    return _override_get_session


@pytest.fixture(scope="function")
async def client(override_get_session):
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as client:
        yield client


# тесты
@pytest.mark.asyncio
async def test_register_user(client):
    response = client.post("/auth/register/",
                           json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


@pytest.mark.asyncio
async def test_user_login(client):
    response = client.post("/auth/login/", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_currencies_list(client):
    access_token = await get_access_token(client)
    response = client.get("/currency/list", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "currencies" in response.json()


@pytest.mark.asyncio
async def test_currency_exchange(client):
    access_token = await get_access_token(client)
    response = client.get("/currency/exchange?base=USD&target=EUR&amount=100",
                          headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "result" in response.json()
