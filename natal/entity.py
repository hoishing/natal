from natal.enums import Sign, Planet, Asteroid, Points
from pydantic import BaseModel


class Entity(BaseModel):
    """astrological entity in natal chart"""

    body: Planet | Asteroid | Points
    """celestial body"""

    degree: float
    """decimal degree, between 0 and 359.99"""

    retro: bool
    """is retrograde or not"""

    @property
    def signed_deg(self) -> int:
        """degree in sign, between 0 and 29"""
        return int(self.degree % 30)

    @property
    def sign(self) -> Sign:
        """sign of the entity"""
        return Sign(int(self.degree // 30) + 1)

    @property
    def minute(self) -> int:
        """minute of the entity, between 0 and 59"""
        minutes = (self.degree % 30 - self.signed_deg) * 60
        round_min = round(minutes)
        return round_min if round_min != 60 else 59

    @property
    def rx(self) -> str | None:
        """Retrograde symbol"""
        return "℞" if self.retro else None

    @property
    def dms(self) -> str:
        """Degree Minute Second representation of the position"""
        base = f"{self.signed_deg}° {self.minute}'"
        return f"{base} {self.rx}" if self.rx else base

    @property
    def signed_dms(self) -> str:
        """Degree Minute representation with sign"""
        base = f"{self.signed_deg} {self.sign.symbol} {self.minute}"
        return f"{base} {self.rx}" if self.rx else base
