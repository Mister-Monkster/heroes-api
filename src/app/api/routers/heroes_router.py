from fastapi import APIRouter, HTTPException

from src.app.dependencies.dependencies import ServiceDep

from src.app.pydantic_models.models import HeroSchema, HeroResponse, HeroDep

router = APIRouter(prefix='/hero')


@router.post("/")
async def save_hero(name: str, service: ServiceDep) -> HeroResponse:
    hero = await service.save_hero(name)
    if hero is None:
        raise HTTPException(status_code=404, detail="Герой не найден. Возможно такого героя не существует.")
    return hero


@router.get("/")
async def get_hero(hero: HeroDep, service: ServiceDep) -> list[HeroResponse]:
    heroes = await service.get_heroes(hero)
    if not heroes or heroes is None:
        raise HTTPException(status_code=404, detail='Героев с такими параметрами нет в базе данных.')
    return heroes