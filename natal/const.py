from typing import Literal, Iterable
from natal.utils import DotDict


class BodyDict(DotDict):
    name: Iterable[str]
    symbol: Iterable[str]
    value: list[int]
    color: list[str]


class SignMember(BodyDict):
    ruler: list[str]
    quality: list[str]
    element: list[str]
    polarity: list[str]


PlanetName = Literal[
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
ExtraName = Literal["chiron", "mean_node"]
PointName = Literal["mean_node"]
ElementName = Literal["fire", "earth", "air", "water"]
QualityName = Literal["cardinal", "fixed", "mutable"]
PolarityName = Literal["positive", "negative"]
SignName = Literal[
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]
HouseName = Literal[
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
]

AspectName = Literal["conjunction", "opposition", "trine", "square", "sextile"]

PLANETS = BodyDict(
    name=PlanetName.__args__,
    symbol="☉☽☿♀♂♃♄♅♆♇",
    value=list(range(10)),
    color="fire water air earth fire fire earth air water water".split(),
)

ASPECTS = BodyDict(
    name=AspectName.__args__,
    symbol="☌☍△□⚹",
    value=[0, 180, 120, 90, 60],
    color=["others", "water", "air", "fire", "points"],
)

ELEMENTS = BodyDict(
    name=ElementName.__args__,
    symbol="🜂🜃🜁🜄",
    value=[0, 1, 2, 3],
    color=["fire", "earth", "air", "water"],
)

QUALITY = BodyDict(
    name=QualityName.__args__,
    symbol="⟑⊟𛰣",
    value=[0, 1, 2],
    color=["fire", "earth", "air"],
)

POLARITY = BodyDict(
    name=PolarityName.__args__,
    symbol=["+", "-"],
    value=[1, -1],
    color=["positive", "negative"],
)

SIGNS = SignMember(
    name=SignName.__args__,
    symbol="♈♉♊♋♌♍♎♏♐♑♒♓",
    value=list(range(1, 13)),
    color=["fire", "earth", "air", "water"] * 3,
    ruler="mars venus mercury moon sun mercury venus pluto jupiter saturn uranus neptune".split(),
    quality=list(QUALITY["name"]) * 4,
    element=list(ELEMENTS["name"]) * 3,
    polarity=list(POLARITY["name"]) * 6,
)

HOUSES = BodyDict(
    name=HouseName.__args__,
    symbol=[str(i) for i in range(1, 13)],
    value=list(range(1, 13)),
    color=["fire", "earth", "air", "water"] * 3,
)

EXTRAS = BodyDict(
    name=ExtraName.__args__,
    symbol="⚷☊",
    value=[15, 10],
    color=["asteroids", "points"],
)
