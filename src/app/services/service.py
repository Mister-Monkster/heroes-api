from httpx import AsyncClient

from src.config import get_api_access
from src.app.db.repository.repository import Repository
from src.app.pydantic_models.models import HeroSchema

from src.app.pydantic_models.models import HeroResponse, HeroGet


class Service:
    def __init__(self, repository: Repository):
        self.repository = repository
        self.token = get_api_access()

    async def find_hero_by_name(self, json: dict, name: str):
        heroes = json.get("results")
        if heroes:
            for hero in heroes:
                if hero["name"].lower() == name.lower():
                    hero_schema = HeroSchema.model_validate(hero)
                    return hero_schema
            return heroes[0]
        else:
            return None


    async def save_hero(self, name: str) -> HeroResponse | None:
        url = f"https://superheroapi.com/api/{self.token}/search/{name}"
        async with AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
        try:
            response_json = response.json()
            hero = await self.find_hero_by_name(response_json, name)
            res = await self.repository.add_hero(hero)
            return res
        except AttributeError:
            return None


    async def get_heroes(self, hero: HeroGet) -> list[HeroGet]  | None:
        try:
            res = await self.repository.get_hero(hero)
            return res
        except Exception as e:
            print(e)
            return None
