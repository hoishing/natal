from natal.utils import DotDict


class Body(DotDict):
    name: str
    symbol: str
    value: int
    color: str


class PlanetMember(Body): ...


class AspectMember(Body): ...


class ElementMember(Body): ...


class QualityMember(Body): ...


class PolarityMember(Body): ...


class HouseMember(Body): ...


class ExtraMember(Body): ...


class VertexMember(Body): ...


class SignMember(Body):
    ruler: str
    classic_ruler: str
    quality: str
    element: str
    polarity: str


# utils ==================================


def get_member(raw_data: dict, name: str) -> DotDict:
    idx = raw_data["name"].index(name)
    member = {key: raw_data[key][idx] for key in raw_data.keys()}
    return DotDict(**member)


def get_members(raw_data: dict) -> list[DotDict]:
    return [get_member(raw_data, name) for name in raw_data["name"]]


# Raw Data ===============================

# fmt: off
PLANET_NAMES = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]
EXTRA_NAMES = ["chiron", "mean_node"]
ELEMENT_NAMES = ["fire", "earth", "air", "water"]
QUALITY_NAMES = ["cardinal", "fixed", "mutable"]
POLARITY_NAMES = ["positive", "negative"]
SIGN_NAMES = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
HOUSE_NAMES = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
ASPECT_NAMES = ["conjunction", "opposition", "trine", "square", "sextile"]
VERTEX_NAMES = ["asc", "mc", "ic", "dsc"]
# fmt: on

PLANETS = dict(
    name=PLANET_NAMES,
    symbol="☉☽☿♀♂♃♄♅♆♇",
    value=list(range(10)),
    color="fire water air earth fire fire earth air water water".split(),
)

ASPECTS = dict(
    name=ASPECT_NAMES,
    symbol="☌☍△□⚹",
    value=[0, 180, 120, 90, 60],
    color=["others", "water", "air", "fire", "points"],
)

ELEMENTS = dict(
    name=ELEMENT_NAMES,
    symbol="🜂🜃🜁🜄",
    value=[0, 1, 2, 3],
    color=["fire", "earth", "air", "water"],
)

QUALITY = dict(
    name=QUALITY_NAMES,
    symbol="⟑⊟𛰣",
    value=[0, 1, 2],
    color=["fire", "earth", "air"],
)

POLARITY = dict(
    name=POLARITY_NAMES,
    symbol=["+", "-"],
    value=[1, -1],
    color=["positive", "negative"],
)

SIGNS = dict(
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

HOUSES = dict(
    name=HOUSE_NAMES,
    symbol=[str(i) for i in range(1, 13)],
    value=list(range(1, 13)),
    color=["fire", "earth", "air", "water"] * 3,
)

EXTRAS = dict(
    name=EXTRA_NAMES,
    symbol="⚷☊",
    value=[15, 10],
    color=["asteroids", "points"],
)

VERTICES = dict(
    name=VERTEX_NAMES,
    symbol=["Asc", "MC", "IC", "Dsc"],
    value=[1, 4, 7, 10],
    color=["fire", "water", "air", "earth"],
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
VERTEX_MEMBERS = get_members(VERTICES)
