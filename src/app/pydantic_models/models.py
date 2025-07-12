from typing import Annotated, Optional

from fastapi.params import Depends
from pydantic import BaseModel, ConfigDict, Field


class PowerStatsSchema(BaseModel):
    intelligence: int = Field(default=0, le=100, ge=0)
    strength: int = Field(default=0, le=100, ge=0)
    speed: int = Field(default=0, le=100, ge=0)
    durability: int = Field(default=0, le=100, ge=0)
    power: int = Field(default=0, le=100, ge=0)
    combat: int = Field(default=0, le=100, ge=0)

    model_config = ConfigDict(from_attributes=True)


class HeroSchema(BaseModel):
    name: str
    powerstats: PowerStatsSchema


class HeroResponse(PowerStatsSchema):
    name: str

    model_config = ConfigDict(from_attributes=True)


class HeroGet(PowerStatsSchema):
    name: Optional[str] = ""

HeroDep = Annotated[HeroGet, Depends()]




