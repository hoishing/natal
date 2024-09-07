from typing import Literal
from natal.utils import BaseDict
import re

# Names and its Types

# fmt: off
PlanetType = Literal["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
PLANET_NAMES = list(PlanetType.__args__)
ExtraType = Literal["chiron", "mean_node", "asc", "mc"]
EXTRA_NAMES = list(ExtraType.__args__)
ElementType = Literal["fire", "earth", "air", "water"]
ELEMENT_NAMES = list(ElementType.__args__)
QualityType = Literal["cardinal", "fixed", "mutable"]
QUALITY_NAMES = list(QualityType.__args__)
PolarityType = Literal["positive", "negative"]
POLARITY_NAMES = list(PolarityType.__args__)
SignType = Literal["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
SIGN_NAMES = list(SignType.__args__)
HouseType = Literal["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
HOUSE_NAMES = list(HouseType.__args__)
AspectType = Literal["conjunction", "opposition", "trine", "square", "sextile"]
ASPECT_NAMES = list(AspectType.__args__)
# fmt: on

# Types ==================================


class Body(BaseDict):
    name: str
    symbol: str
    value: int
    color: str


class PlanetMember(Body):
    name: PlanetType


class AspectMember(Body):
    name: AspectType


class ElementMember(Body):
    name: ElementType


class QualityMember(Body):
    name: QualityType


class PolarityMember(Body):
    name: PolarityType


class HouseMember(Body):
    name: HouseType


class ExtraMember(Body):
    name: ExtraType


class SignMember(Body):
    name: SignType
    ruler: str
    classic_ruler: str
    quality: str
    element: str
    polarity: str


class Raw[T](Body):
    name: list[str]
    symbol: list[str] | str
    value: list[int]
    color: list[str]


class RawSign[T](Raw[T]):
    ruler: list[str]
    classic_ruler: list[str]
    quality: list[str]
    element: list[str]
    polarity: list[str]


# utils ==================================


def get_member[T](raw: Raw[T], name: str) -> T:
    idx = raw.name.index(name)
    member = {key: raw[key][idx] for key in raw.model_fields.keys()}
    raw_class_name = str(type(raw))
    member_class_name = re.search(r"\[([^\]]+)\]", raw_class_name).group(1)
    member_class = globals()[member_class_name]
    return member_class(**member)


def get_members[T](raw: Raw[T]) -> list[T]:
    return [get_member(raw, name) for name in raw.name]


# Raw Data ===============================


PLANETS = Raw[PlanetMember](
    name=PLANET_NAMES,
    symbol="☉☽☿♀♂♃♄♅♆♇",
    value=list(range(10)),
    color="fire water air earth fire fire earth air water water".split(),
)

ASPECTS = Raw[AspectMember](
    name=ASPECT_NAMES,
    symbol="☌☍△□⚹",
    value=[0, 180, 120, 90, 60],
    color=["others", "water", "air", "fire", "points"],
)

ELEMENTS = Raw[ElementMember](
    name=ELEMENT_NAMES,
    symbol="🜂🜃🜁🜄",
    value=[0, 1, 2, 3],
    color=["fire", "earth", "air", "water"],
)

QUALITY = Raw[QualityMember](
    name=QUALITY_NAMES,
    symbol="⟑⊟𛰣",
    value=[0, 1, 2],
    color=["fire", "earth", "air"],
)

POLARITY = Raw[PolarityMember](
    name=POLARITY_NAMES,
    symbol=["+", "-"],
    value=[1, -1],
    color=["positive", "negative"],
)

SIGNS = RawSign[SignMember](
    name=SIGN_NAMES,
    symbol="♈♉♊♋♌♍♎♏♐♑♒♓",
    value=list(range(1, 13)),
    color=["fire", "earth", "air", "water"] * 3,
    ruler="mars venus mercury moon sun mercury venus pluto jupiter saturn uranus neptune".split(),
    classic_ruler="mars venus mercury moon sun mercury venus mars jupiter saturn saturn jupiter".split(),
    quality=list(QUALITY["name"]) * 4,
    element=list(ELEMENTS["name"]) * 3,
    polarity=list(POLARITY["name"]) * 6,
)

HOUSES = Raw[HouseMember](
    name=HOUSE_NAMES,
    symbol=[str(i) for i in range(1, 13)],
    value=list(range(1, 13)),
    color=["fire", "earth", "air", "water"] * 3,
)

EXTRAS = Raw[ExtraMember](
    name=EXTRA_NAMES,
    symbol="⚷ ☊ Asc MC",
    value=[15, 10, -2, -3],
    color=["asteroids", "points", "fire", "earth"],
)

# Derived Members =================================

PLANET_MEMBERS = get_members(PLANETS)
ASPECT_MEMBERS = get_members(ASPECTS)
ELEMENT_MEMBERS = get_members(ELEMENTS)
QUALITY_MEMBERS = get_members(QUALITY)
POLARITY_MEMBERS = get_members(POLARITY)
SIGN_MEMBERS = get_members(SIGNS)
HOUSE_MEMBERS = get_members(HOUSES)
EXTRA_MEMBERS = get_members(EXTRAS)
