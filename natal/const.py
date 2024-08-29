from pydantic import BaseModel

BODIES = dict(
    name="sun moon mercury venus mars jupiter saturn uranus neptune pluto chiron asc mc",
    symbol="☉ ☽ ☿ ♀ ♂ ♃ ♄ ♅ ♆ ♇ ⚷ Asc MC",
    swe_id=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, None, None],
)

HOUSE_SYS = dict(
    name="placidus koch equal campanus regiomontanus porphyry whole_sign",
    swe_id="P K E C R O W",
)

ASPECTS = dict(
    name="conjunction opposition trine square sextile",
    angle=[0, 180, 120, 90, 60],
)

ELEMENT = dict(
    name="fire earth air water",
    symbol="🜂🜃🜁🜄",
)

QUALITY = dict(
    name="cardinal fixed mutable",
    symbol="⟑⊟𛰣",
)

POLARITY = dict(
    name="positive negative",
    symbol=["+", "-"],
)

SIGN = dict(
    name="aries taurus gemini cancer leo virgo libra scorpio sagittarius capricorn aquarius pisces",
    symbol="♈♉♊♋♌♍♎♏♐♑♒♓",
    ruler="mars venus mercury moon sun mercury venus pluto jupiter saturn uranus neptune",
    quality=QUALITY["name"].split() * 4,
    element=ELEMENT["name"].split() * 3,
    polarity=POLARITY["name"].split() * 6,
)
