import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

from tests.conftest import mock_hero_service


@pytest.mark.asyncio
async def test_save_hero(async_client: AsyncClient, mock_hero_service):
    response = await async_client.post("/hero/", params={"name": "Superman"})
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Superman"
    assert data["intelligence"] == 94
    mock_hero_service.save_hero.assert_called_once()


@pytest.mark.asyncio
async def test_negative_save_hero(async_client: TestClient, mock_hero_service):
    response = await async_client.post("/hero/", params={"name": "fasfa"})
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == "Герой не найден. Возможно такого героя не существует."
    mock_hero_service.save_hero.assert_called_once()


@pytest.mark.asyncio
async def test_get_heroes_filter_by_name(async_client: AsyncClient, mock_hero_service):
    response = await async_client.get("/hero/", params={"name": "superman"})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == "Superman"
    assert len(data) == 1
    mock_hero_service.get_heroes.assert_called_once()

@pytest.mark.asyncio
async def test_get_heroes_filter_by_param(async_client: AsyncClient, mock_hero_service):
    response = await async_client.get("/hero/", params={"speed": 25})
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    mock_hero_service.get_heroes.assert_called_once()


@pytest.mark.asyncio
async def test_negative_get_heroes(async_client: AsyncClient, mock_hero_service):
    response = await async_client.get("/hero/", params={"name": "batman", "combat": 91})
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == "Героев с такими параметрами нет в базе данных."
    mock_hero_service.get_heroes.assert_called_once()




