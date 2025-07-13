from typing import Annotated, Optional

from fastapi.params import Depends
from pydantic import BaseModel, ConfigDict, Field


class PowerStatsSchema(BaseModel):
    intelligence: int = Field(default=0, le=100, ge=0, description='Интеллект')
    strength: int = Field(default=0, le=100, ge=0, description="Сила")
    speed: int = Field(default=0, le=100, ge=0, description="Cкорость")
    durability: int = Field(default=0, le=100, ge=0, description="Прочность")
    power: int = Field(default=0, le=100, ge=0, description="Мощь")
    combat: int = Field(default=0, le=100, ge=0, description="Боевые навыки")

    model_config = ConfigDict(from_attributes=True)


class HeroSchema(BaseModel):
    name: str = Field(max_length=128, description="Имя")
    powerstats: PowerStatsSchema


class HeroResponse(PowerStatsSchema):
    name: str = Field(max_length=128, description="Имя")

    model_config = ConfigDict(from_attributes=True)


class HeroGet(PowerStatsSchema):
    name: Optional[str] = Field(default="", max_length=128, description="Имя")

HeroDep = Annotated[HeroGet, Depends()]




