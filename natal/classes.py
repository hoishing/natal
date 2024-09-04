from natal.const import *
from pydantic import BaseModel, Field, field_validator
from typing import NamedTuple
from enum import StrEnum
from math import floor


class Entity(BaseModel):
    name: str
    symbol: str
    value: int | str
    color: str


class MovableEntity(Entity):
    degree: float = Field(..., gt=0, lt=360)
    retro: bool = False

    @field_validator("degree")
    @classmethod
    def round_degree(cls, degree):
        return round(degree, 4)

    @property
    def signed_deg(self) -> int:
        """degree in sign, between 0 and 29"""
        return int(self.degree % 30)

    @property
    def minute(self) -> int:
        """minute of the entity, between 0 and 59"""
        minutes = (self.degree % 30 - self.signed_deg) * 60
        return floor(minutes)

    @property
    def rx(self) -> str | None:
        """Retrograde symbol"""
        return "℞" if self.retro else None

    @property
    def dms(self) -> str:
        """Degree Minute Second representation of the position"""
        op = [f"{self.signed_deg}°", f"{self.minute}'"]
        if self.rx:
            op.append(self.rx)
        return " ".join(op)

    @property
    def signed_dms(self) -> str:
        """Degree Minute representation with sign"""
        idx = int(self.degree // 30)
        symbol = SIGNS["symbol"][idx]
        op = [f"{self.signed_deg}", symbol, f"{self.minute}'"]
        if self.rx:
            op.append(self.rx)
        return " ".join(op)


class Sign(MovableEntity):
    name: SignName
    ruler: str
    quality: str
    element: str
    polarity: str


class Aspect(NamedTuple):
    entity1: MovableEntity
    entity2: MovableEntity
    aspect_type: Entity


class HouseSys(StrEnum):
    Placidus = "P"
    Koch = "K"
    Equal = "E"
    Campanus = "C"
    Regiomontanus = "R"
    Porphyry = "P"
    Whole_Sign = "W"
