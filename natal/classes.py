from natal.const import *
from pydantic import BaseModel, Field, field_validator
from typing import NamedTuple
from enum import StrEnum
from math import floor
from natal.utils import DotDict


class SignMember(DotDict):
    name: SignName
    symbol: str
    ruler: str
    element: str
    quality: str
    polarity: str


class Body(BaseModel):
    name: str
    symbol: str
    value: int | str
    color: str


class MovableBody(Body):
    degree: float = Field(None, gt=0, lt=360)
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
        """minute of the body, between 0 and 59"""
        minutes = (self.degree % 30 - self.signed_deg) * 60
        return floor(minutes)

    @property
    def rx(self) -> str:
        """Retrograde symbol"""
        return "℞" if self.retro else ""

    @property
    def sign(self) -> SignMember:
        """Return sign name, symbol, element, quality, and polarity."""
        idx = int(self.degree // 30)
        return SignMember(
            **{prop: SIGNS[prop][idx] for prop in SignMember.__annotations__.keys()}
        )

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
        op = [f"{self.signed_deg}", self.sign.symbol, f"{self.minute}'"]
        if self.rx:
            op.append(self.rx)
        return " ".join(op)


class Sign(MovableBody):
    name: SignName
    ruler: str
    quality: str
    element: str
    polarity: str


class House(MovableBody):
    ruler: str
    ruler_sign: str
    ruler_house: int


class Aspect(NamedTuple):
    body1: MovableBody
    body2: MovableBody
    aspect_type: Body
    approaching: bool = None
    orb: float = None


class HouseSys(StrEnum):
    Placidus = "P"
    Koch = "K"
    Equal = "E"
    Campanus = "C"
    Regiomontanus = "R"
    Porphyry = "P"
    Whole_Sign = "W"
