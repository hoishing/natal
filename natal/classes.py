from natal.const import *
from enum import StrEnum
from math import floor


class MovableBody(Body):
    degree: float = 0
    speed: float = 0
    normalized_degree: float = 0

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
    def retro(self) -> bool:
        """Retrograde status"""
        return self.speed < 0

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
        op = [f"{self.signed_deg:02d}°", f"{self.minute:02d}'"]
        if self.rx:
            op.append(self.rx)
        return "".join(op)

    @property
    def signed_dms(self) -> str:
        """Degree Minute representation with sign"""
        op = [f"{self.signed_deg:02d}°", self.sign.symbol, f"{self.minute:02d}'"]
        if self.rx:
            op.append(self.rx)
        return "".join(op)


class Planet(MovableBody): ...


class Extra(MovableBody): ...


class Vertex(MovableBody): ...


class Aspectable(MovableBody): ...


class Sign(MovableBody):
    ruler: str
    classic_ruler: str
    quality: str
    element: str
    polarity: str


class House(MovableBody): ...


class HouseWithRuler(House):
    ruler: str = None
    ruler_sign: str = None
    ruler_house: int = None
    classic_ruler: str = None
    classic_ruler_sign: str = None
    classic_ruler_house: int = None


class Aspect(DotDict):
    body1: Aspectable
    body2: Aspectable
    aspect_member: AspectMember
    applying: bool = None
    orb: float = None


class HouseSys(StrEnum):
    Placidus = "P"
    Koch = "K"
    Equal = "E"
    Campanus = "C"
    Regiomontanus = "R"
    Porphyry = "P"
    Whole_Sign = "W"
