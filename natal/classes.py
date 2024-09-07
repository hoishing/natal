from natal.const import *
from pydantic import Field, field_validator
from typing import NamedTuple
from enum import StrEnum
from math import floor


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
        return SIGN_MEMBERS[idx]

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


class Planet(MovableBody):
    name: PlanetType


class Extra(MovableBody):
    name: ExtraType


class Aspectable(MovableBody):
    name: PlanetType | ExtraType


class Sign(MovableBody):
    name: SignType
    ruler: str
    classic_ruler: str
    quality: str
    element: str
    polarity: str


class House(MovableBody):
    name: HouseType


class HouseWithRuler(House):
    ruler: str = None
    ruler_sign: str = None
    ruler_house: int = None
    classic_ruler: str = None
    classic_ruler_sign: str = None
    classic_ruler_house: int = None


class Aspect(NamedTuple):
    body1: Aspectable
    body2: Aspectable
    aspect_type: AspectType
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
