from enum import auto, StrEnum, IntEnum


class Sign(IntEnum):
    """12 zodiac signs represented as 1-indexed IntEnum

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
    def ruler(self) -> "Planet":
        """ruler of the sign"""
        return [
            Planet.mars,
            Planet.venus,
            Planet.mercury,
            Planet.moon,
            Planet.sun,
            Planet.mercury,
            Planet.venus,
            Planet.mars,
            Planet.jupiter,
            Planet.saturn,
            Planet.uranus,
            Planet.neptune,
        ][self - 1]


class Modality(IntEnum):
    """3 modalities of Quadruplicity represented as 1-indexed IntEnum"""

    cardinal = 1
    fixed = 2
    mutable = 3

    @property
    def symbol(self) -> str:
        return "⟑⊟𛰣"[self - 1]

    @property
    def signs(self) -> list[Sign]:
        return [Sign(i) for i in range(self, 13, 3)]


class Element(IntEnum):
    """4 elements of Triplicity represented as 1-indexed IntEnum"""

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


class Polarity(IntEnum):
    """2 polarities represented as 0-indexed IntEnum"""

    positive = 0
    negative = 1

    @property
    def symbol(self) -> str:
        return "+-"[self.value]

    @property
    def signs(self):
        return [Sign(i) for i in range(self, 12, 2)]


class Planet(IntEnum):
    """10 planets and luminaries represented as 1-indexed IntEnum"""

    sun = 0
    moon = auto()
    mercury = auto()
    venus = auto()
    mars = auto()
    jupiter = auto()
    saturn = auto()
    uranus = auto()
    neptune = auto()
    pluto = auto()

    @property
    def symbol(self) -> str:
        """astrological symbol of the planet"""
        return "☉☽☿♀♂♃♄♅♆♇"[self]

    @property
    def swe(self) -> str:
        """swiss ephemeris constant"""
        return "SE_" + self.name.upper()

    @property
    def ruling(self) -> list[Sign]:
        """signs ruled by the planet"""
        return (
            [Sign.aries],
            [Sign.cancer],
            [Sign.gemini, Sign.virgo],
            [Sign.taurus, Sign.libra],
            [Sign.aries],
            [Sign.sagittarius],
            [Sign.capricorn],
            [Sign.aquarius],
            [Sign.pisces],
            [Sign.scorpio],
        )[self]


class ExtraPoints(IntEnum):
    """Extra points in astrology represented as 0-indexed IntEnum"""

    chiron = 0
    mean_node = auto()
    ascendant = auto()
    midheaven = auto()
    descendant = auto()
    imum_coeli = auto()

    @property
    def symbol(self) -> str:
        return "⚷ ☊ Asc MC Dsc IC".split()[self]


class House(IntEnum):
    """12 houses represented as 1-indexed IntEnum"""

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
    def sign(self):
        """sign on the cusp of the house"""
        return Sign(self)

    @property
    def ruler(self):
        """ruler of the house"""
        return Sign(self).ruler


class Aspect(StrEnum):
    """Astrological aspects represented as StrEnum"""

    conj = "Conjunction"
    opp = "Opposition"
    tri = "Trine"
    squ = "Square"
    sex = "Sextile"


AstroEnums = (
    Sign | Modality | Element | Polarity | Planet | ExtraPoints | House | Aspect
)
"""Union of all astrological entity enums"""
