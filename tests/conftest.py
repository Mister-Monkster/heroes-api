from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from src.app.dependencies.dependencies import get_service
from src.app.pydantic_models.models import HeroGet

from src.app.services.service import Service
from main import app


async def save_hero_side_effect(name: str):
    if name.lower() == "superman":
        return {
            "intelligence": 94,
            "strength": 100,
            "speed": 100,
            "durability": 100,
            "power": 100,
            "combat": 85,
            "name": "Superman"
        }
    else:
        return None

async def get_heroes_side_effect(params: HeroGet):
    if params.speed >= 25:
        return [
                {
                    "intelligence": 81,
                    "strength": 40,
                    "speed": 29,
                    "durability": 55,
                    "power": 63,
                    "combat": 90,
                    "name": "Batman"
                },
                {
                    "intelligence": 94,
                    "strength": 100,
                    "speed": 100,
                    "durability": 100,
                    "power": 100,
                    "combat": 85,
                    "name": "Superman"
                }
              ]
    elif params.name.lower() == 'superman':
        return [
            {
                "intelligence": 94,
                "strength": 100,
                "speed": 100,
                "durability": 100,
                "power": 100,
                "combat": 85,
                "name": "Superman"
            }
        ]
    else:
        return []


@pytest_asyncio.fixture(scope="function", autouse=True)
async def mock_hero_service() -> AsyncMock:
    mock_service = AsyncMock(spec=Service)
    mock_service.save_hero.side_effect = save_hero_side_effect
    mock_service.get_heroes.side_effect = get_heroes_side_effect
    return mock_service


@pytest_asyncio.fixture(scope="function", autouse=True)
async def configured_app() -> FastAPI:
    return app


@pytest_asyncio.fixture(scope="function", autouse=True)
def override_dependencies(configured_app: FastAPI, mock_hero_service: AsyncMock):
    configured_app.dependency_overrides[get_service] = lambda: mock_hero_service
    yield
    configured_app.dependency_overrides = {}


@pytest_asyncio.fixture(scope="function")
async def async_client(configured_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    BASE_URL = "http://test"
    async with AsyncClient(
        transport=ASGITransport(app=configured_app),
        base_url=BASE_URL
    ) as client:
        yield client

