from natal.enums import Sign
from pydantic import Field, field_validator
from math import floor
from typing import Self
from natal.const import Entity


class Position(Entity):
    """astrological entity in natal chart"""

    degree: float | None = Field(None, ge=0, le=359.99)
    """decimal degree, between 0 and 359.99"""

    retro: bool = False
    """is retrograde or not"""

    @classmethod
    def create(cls, entity: Entity) -> Self:
        return Self(name=entity.name, symbol=entity.symbol, color=entity.color)

    @field_validator("degree")
    @classmethod
    def round_degree(cls, degree):
        return round(degree, 2)

    @property
    def sign(self) -> Sign:
        """sign of the entity"""
        return Sign(int(self.degree // 30) + 1)

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
        op = [f"{self.signed_deg}", f"{self.sign.symbol}", f"{self.minute}'"]
        if self.rx:
            op.append(self.rx)
        return " ".join(op)
