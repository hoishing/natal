from natal.data import Data
from datetime import datetime
from pytest import fixture


@fixture(scope="module")
def data() -> Data:
    return Data(name="shing", city="hong kong", dt="1976-04-20 18:58")


@fixture
def planets() -> dict[str, str]:
    return dict(
        sun="00°♉26'",
        moon="19°♑47'",
        mercury="18°♉30'",
        venus="14°♈49'",
        mars="15°♋54'",
        jupiter="05°♉52'",
        saturn="26°♋31'",
        uranus="05°♏19'℞",
        neptune="13°♐38'℞",
        pluto="09°♎47'℞",
    )


@fixture
def houses() -> dict[str, str]:
    return dict(
        one="20°♎32'",
        two="19°♏43'",
        three="19°♐49'",
        four="20°♑36'",
        five="21°♒53'",
        six="22°♓29'",
        seven="20°♈32'",
        eight="19°♉43'",
        nine="19°♊49'",
        ten="20°♋36'",
        eleven="21°♌54'",
        twelve="22°♍29'",
    )


@fixture
def others() -> dict[str, str]:
    return dict(
        chiron="27°♈49'",
        mean_node="13°♏25'℞",
        asc="20°♎32'",
        mc="20°♋36'",
        house_sys="P",
    )


@fixture
def signs() -> dict:
    return dict(
        aries=(159.45, "mars", "fire", "cardinal", "fire", "positive"),
        taurus=(189.45, "venus", "earth", "fixed", "earth", "negative"),
        gemini=(219.45, "mercury", "air", "mutable", "air", "positive"),
        cancer=(249.45, "moon", "water", "cardinal", "water", "negative"),
        leo=(279.45, "sun", "fire", "fixed", "fire", "positive"),
        virgo=(309.45, "mercury", "earth", "mutable", "earth", "negative"),
        libra=(339.45, "venus", "air", "cardinal", "air", "positive"),
        scorpio=(9.45, "pluto", "water", "fixed", "water", "negative"),
        sagittarius=(39.45, "jupiter", "fire", "mutable", "fire", "positive"),
        capricorn=(69.45, "saturn", "earth", "cardinal", "earth", "negative"),
        aquarius=(99.45, "uranus", "air", "fixed", "air", "positive"),
        pisces=(129.45, "neptune", "water", "mutable", "water", "negative"),
    )


def test_lat_lon(data: Data) -> None:
    assert round(data.lat, 2) == 22.28
    assert round(data.lon, 2) == 114.17


def test_data_input(data: Data) -> None:
    assert data.name == "shing"
    assert data.city == "hong kong"
    assert data.dt == datetime(1976, 4, 20, 18, 58)


def test_planet(data: Data, planets: dict[str, str]) -> None:
    for planet in data.planets:
        assert planet.name in planets
        assert planet.signed_dms == planets[planet.name]


def test_houses(data: Data, houses: dict[str, str]) -> None:
    for house in data.houses:
        assert house.name in houses
        assert house.signed_dms == houses[house.name]


def test_asc_mc(data: Data, others: dict[str, str]) -> None:
    assert data.asc.signed_dms == others["asc"]
    assert data.mc.signed_dms == others["mc"]
    assert data.chiron.signed_dms == others["chiron"]
    assert data.mean_node.signed_dms == others["mean_node"]
    assert data.house_sys == others["house_sys"]


def test_signs(data: Data, signs: dict) -> None:
    for sign in data.signs:
        assert sign.name in signs
        assert round(sign.degree, 2) == signs[sign.name][0]
        assert sign.ruler == signs[sign.name][1]
        assert sign.color == signs[sign.name][2]
        assert sign.quality == signs[sign.name][3]
        assert sign.element == signs[sign.name][4]
        assert sign.polarity == signs[sign.name][5]


def test_normalized_bodies(data: Data) -> None:
    for body in data.aspectable:
        assert body.normalized_degree == data.normalize(body.degree)
