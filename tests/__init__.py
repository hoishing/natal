from pytest import fixture
from natal.data import Data
from natal.config import Config

person1 = {
    "name": "shing",
    "city": "hong kong",
    "dt": "1976-04-20 18:58",
}

person2 = {
    "name": "belle",
    "city": "hong kong",
    "dt": "2011-01-23 08:44",
}

option = {
    "display": {"chiron": True, "mean_node": True},
    "orb": {"conjunction": 8, "opposition": 7, "trine": 6, "square": 6, "sextile": 5},
    "composite_orb": {"conjunction": 6, "opposition": 6, "trine": 6, "square": 6, "sextile": 4},
}

config = Config(**option)


@fixture(scope="package")
def data1():
    return Data(**person1, config=config)


@fixture(scope="package")
def data2():
    return Data(**person2, config=config)
