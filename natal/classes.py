from pydantic import BaseModel
from typing import Literal
from natal.config import CONFIG

Planet = Literal[
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
]
PlanetSym = Literal["☉", "☽", "☿", "♀", "♂", "♃", "♄", "♅", "♆", "♇"]
Asteroid = Literal["chiron", "pholus", "ceres", "pallas", "juno", "vesta"]
AsteroidSym = Literal["⚷", "⯛", "⚳", "⚴", "⚵", "⚶"]
Others = Literal["mean node", "Asc", "MC"]
EntitySym = Literal["☉", "☽", "☿", "♀", "♂", "♃", "♄", "♅", "♆", "♇", "⚷", "Asc", "MC"]
ElementName = Literal["fire", "earth", "air", "water"]
QualityName = Literal["cardinal", "fixed", "mutable"]


class Element(BaseModel):
    """element of the zodiac sign"""

    name: ElementName

    @property
    def color(self) -> str:
        """color of the element"""
        return dict(
            fire = CONFIG.colors.red,
            earth = CONFIG.colors.yellow,
            air = CONFIG.colors.green,
            water = CONFIG.colors.blue
        ).get(self.name)        

class Quality(BaseModel):
    """quality of the zodiac sign"""

    name: QualityName

    @property
    def color(self) -> str:
        """color of the quality"""
        return dict(
            cardinal = CONFIG.colors.red,
            fixed = CONFIG.colors.yellow,
            mutable = CONFIG.colors.blue
        ).get(self.name)
    
    @property
    def symbol(self) -> str:
        """symbol of the quality"""

        return dict(
            cardinal = "♈",
            fixed = "♉",
            mutable = "♊"
        ).get(self.name)



class Entity(BaseModel):
    """astrological entity with degree including planets, asteroids, Asc and MC"""

    name: Planet | Asteroid | Others
    degree: float  # decimal degree
    retrograde: bool

    @property
    def symbol(self) -> EntitySym:
        """astrological symbol of the entity"""
        ...

    @property
    def color(self) -> str:
        """color of the entity"""
        ...

    @property
    def sign_degree(self) -> int:
        """degree in sign, 0-29"""
        ...

    @property
    def sign(self) -> str:
        """sign of the entity"""
        ...

    @property
    def minutes(self) -> int:
        """minutes of the entity, 0-59"""
        ...

    @property
    def dms(self) -> str:
        """degree, minute"""
        retro = "℞" if self.retrograde else ""
        return f"{self.sign_degree}°{self.minutes}'{retro}"

    @property
    def signed_dms(self) -> str:
        """degree, sign, minute"""
        retro = " ℞" if self.retrograde else ""
        return f"{self.sign_degree} {self.symbol} {self.minutes}{retro}"


class Sign(BaseModel):
    """a zodiac sign"""

    name: str
    symbol: str
    ruler: str
    element: str
    quality: str
    polarity: str

    # @property
    # def color(self) ->  str:
    #     """color of the sign"""
    #     CONFIG.


class House(BaseModel):
    """a house with degree and ruling sign"""

    number: int
    cusp: float
    sign: str
    ruler: list[str]
    color: str


class HouseSys(BaseModel):
    """house system"""

    name: str
    swe_id: str


class Aspect(BaseModel):
    """aspect between two celestial bodies"""

    name: str
    angle: int
    orb: float
