from natal.data import Data
from datetime import datetime
from pytest import fixture
from . import data1


@fixture(scope="module")
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


@fixture(scope="module")
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


@fixture(scope="module")
def others() -> dict[str, str]:
    return dict(
        chiron="27°♈49'",
        mean_node="13°♏25'℞",
        asc="20°♎32'",
        mc="20°♋36'",
        house_sys="P",
    )


@fixture(scope="module")
def signs() -> dict:
    return dict(
        aries=(0, "mars", "fire", "cardinal", "fire", "positive"),
        taurus=(30, "venus", "earth", "fixed", "earth", "negative"),
        gemini=(60, "mercury", "air", "mutable", "air", "positive"),
        cancer=(90, "moon", "water", "cardinal", "water", "negative"),
        leo=(120, "sun", "fire", "fixed", "fire", "positive"),
        virgo=(150, "mercury", "earth", "mutable", "earth", "negative"),
        libra=(180, "venus", "air", "cardinal", "air", "positive"),
        scorpio=(210, "pluto", "water", "fixed", "water", "negative"),
        sagittarius=(240, "jupiter", "fire", "mutable", "fire", "positive"),
        capricorn=(270, "saturn", "earth", "cardinal", "earth", "negative"),
        aquarius=(300, "uranus", "air", "fixed", "air", "positive"),
        pisces=(330, "neptune", "water", "mutable", "water", "negative"),
    )


def test_lat_lon(data1: Data) -> None:
    assert round(data1.lat, 2) == 22.28
    assert round(data1.lon, 2) == 114.17


def test_data_input(data1: Data) -> None:
    assert data1.name == "shing"
    assert data1.city == "hong kong"
    assert data1.dt == datetime(1976, 4, 20, 18, 58)


def test_planet(data1: Data, planets: dict[str, str]) -> None:
    for planet in data1.planets:
        assert planet.name in planets
        assert planet.signed_dms == planets[planet.name]


def test_houses(data1: Data, houses: dict[str, str]) -> None:
    for house in data1.houses:
        assert house.name in houses
        assert house.signed_dms == houses[house.name]


def test_asc_mc(data1: Data, others: dict[str, str]) -> None:
    assert data1.asc.signed_dms == others["asc"]
    assert data1.mc.signed_dms == others["mc"]
    assert data1.chiron.signed_dms == others["chiron"]
    assert data1.mean_node.signed_dms == others["mean_node"]
    assert data1.house_sys == others["house_sys"]


def test_signs(data1: Data, signs: dict) -> None:
    for sign in data1.signs:
        assert sign.name in signs
        assert round(sign.degree, 2) == signs[sign.name][0]
        assert sign.ruler == signs[sign.name][1]
        assert sign.color == signs[sign.name][2]
        assert sign.quality == signs[sign.name][3]
        assert sign.element == signs[sign.name][4]
        assert sign.polarity == signs[sign.name][5]


def test_normalized_bodies(data1: Data) -> None:
    for body in data1.aspectables:
        assert body.normalized_degree == data1.normalize(body.degree)
