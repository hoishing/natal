"""Enums for signs, modalities, elements, polarities, bodies(planets, asteroid, angles), houses, and aspects

Note: 
    - Sign, Element, Hse, Modality are 1-indexed for astrological convenience
    - `auto()` starts from 1
    - polarities are -1 for negative, 1 for positive
    - aspects value are their respective degrees
"""

from enum import IntEnum, StrEnum, Enum
from abc import ABC, abstractmethod


def pos(member: Enum):
    return list(member.__class__).index(member)

class Body(ABC):
    name: str

    @property
    @abstractmethod
    def symbol(self) -> str:
        pass

    @property
    @abstractmethod
    def color_name(self) -> str:
        pass


class Sign(IntEnum, Body):
    """12 zodiac signs

    Examples:

        >>> Sign.aries
        <Sign.aries: 1>

        - access by value
        >>> Sign(1)
        <Sign.aries: 1>

        - act as int
        >>> "🍏🍊🍌"[Sign(1)]
        '🍊'

        - member properties
        >>> Sign.taurus.symbol
        '♉'

        >>> Sign.gemini.modality
        <Modality.mutable: 3>

        >>> Sign.cancer.element
        <Element.water: 4>

        >>> Sign.leo.polarity
        <Polarity.positive: 0>

        >>> Sign.virgo.ruler
        <Planet.mercury: 2>
    """

    aries = 1
    taurus = 2
    gemini = 3
    cancer = 4
    leo = 5
    virgo = 6
    libra = 7
    scorpio = 8
    sagittarius = 9
    capricorn = 10
    aquarius = 11
    pisces = 12

    @property
    def symbol(self):
        """astrological symbol of the sign"""
        return "♈♉♊♋♌♍♎♏♐♑♒♓"[self - 1]

    @property
    def modality(self) -> "Modality":
        """modality of the sign"""
        return (list(Modality) * 4)[self - 1]

    @property
    def element(self) -> "Element":
        """element of the sign"""
        return (list(Element) * 3)[self - 1]

    @property
    def polarity(self) -> "Polarity":
        """polarity of the sign"""
        return (list(Polarity) * 6)[self - 1]

    @property
    def ruler(self) -> "Planets":
        """ruler of the sign"""
        return [
            Planets.mars,
            Planets.venus,
            Planets.mercury,
            Planets.moon,
            Planets.sun,
            Planets.mercury,
            Planets.venus,
            Planets.mars,
            Planets.jupiter,
            Planets.saturn,
            Planets.uranus,
            Planets.neptune,
        ][self - 1]

    @property
    def color_name(self) -> str:
        return self.element.name


class Modality(IntEnum):
    """3 modalities of Quadruplicity"""

    cardinal = 1
    fixed = 2
    mutable = 3

    @property
    def symbol(self) -> str:
        return "⟑⊟𛰣"[self - 1]

    @property
    def signs(self) -> list[Sign]:
        return [Sign(i) for i in range(self, 13, 3)]

    @property
    def color_name(self) -> str:
        return ["fire", "earth", "air"][self - 1]


class Element(IntEnum):
    """4 elements of Triplicity"""

    fire = 1
    earth = 2
    air = 3
    water = 4

    @property
    def symbol(self) -> str:
        return "🜂🜃🜁🜄"[self - 1]

    @property
    def signs(self) -> list[Sign]:
        return [Sign(i) for i in range(self, 13, 4)]

    @property
    def color_name(self) -> str:
        return self.name


class Polarity(IntEnum):
    """Polarities (-1 for negative, 1 for positive)"""

    positive = 1
    negative = -1

    @property
    def symbol(self) -> str:
        return {1: "+", -1: "-"}[self]

    @property
    def signs(self):
        return [Sign(i) for i in range(1, 13, 2)]


class Planets(IntEnum, Body):
    """celestial bodies, including planets, asteroid and angles.

    both name and value match Swiss Ephemeris constants"""

    sun = 0
    moon = 1
    mercury = 2
    venus = 3
    mars = 4
    jupiter = 5
    saturn = 6
    uranus = 7
    neptune = 8
    pluto = 9

    @property
    def symbol(self) -> str:
        """astrological symbol of the planet"""
        return "☉☽☿♀♂♃♄♅♆♇"[self]

    @property
    def color_name(self) -> str:
        rulers = [s.ruler for s in Sign]
        idx = rulers.index(self)
        return Sign(idx + 1).color_name


class Asteroids(IntEnum, Body):
    """asteroids"""

    chiron = 15
    pholus = 16
    ceres = 17
    pallas = 18
    juno = 19
    vesta = 20

    @property
    def symbol(self) -> str:
        return "⚷⯛⚳⚴⚵⚶"[pos(self)]
    
    @property
    def color_name(self) -> str:
        return self.__class__.__name__.lower()


class Points(IntEnum, Body):
    """celestial points, including nodes and apogees"""

    mean_node = 10

    @property
    def symbol(self) -> str:
        return "☊"[pos(self)]

    @property
    def color_name(self) -> str:
        return self.__class__.__name__.lower()


class HouseType(IntEnum, Body):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    eleven = 11
    twelve = 12

    @property
    def symbol(self) -> str:
        return str(self)

    @property
    def color_name(self) -> str:
        return Sign(self).color_name


class HouseSystem(StrEnum):
    """Astrological house systems, values are Swiss Ephemeris constants"""

    Placidus = "P"
    Koch = "K"
    Porphyry = "O"
    Regiomontanus = "R"
    Campanus = "C"
    Equal = "E"
    Whole_Sign = "W"


class AspectType(IntEnum):
    """Astrological aspects, values are degrees"""

    conjunction = 0
    opposition = 180
    trine = 120
    square = 90
    sextile = 60

    @property
    def symbol(self) -> str:
        return "☌☍△□⚹"[pos(self)]

    @property
    def color_name(self) -> str:
        return ["orange", "blue", "green", "red", "aqua"][pos(self)]
