from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models.models import Hero
from src.app.pydantic_models.models import HeroSchema, HeroGet


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_hero(self, hero: HeroSchema):
        powerstats_dict = hero.powerstats.model_dump()
        stmt = (insert(Hero)
                .values(
                        name=hero.name,
                        **powerstats_dict
                        )
                .on_conflict_do_update(
                                        index_elements=['name'],
                                        set_=powerstats_dict)
                .returning(Hero)
                )
        hero = await self.session.execute(stmt)
        await self.session.commit()
        return hero.scalars().one()


    async def get_hero(self, hero: HeroGet):
        stmt = select(Hero).where(Hero.intelligence >= hero.intelligence,
                                  Hero.durability >= hero.durability,
                                  Hero.power >= hero.power,
                                  Hero.speed >= hero.speed,
                                  Hero.strength >= hero.strength,
                                  Hero.combat >= hero.combat)
        if hero.name:
            stmt = stmt.where(Hero.name == hero.name.title())

        result = await self.session.execute(stmt)
        return result.scalars().all()