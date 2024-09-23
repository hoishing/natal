from pytest import fixture
from natal.data import Data

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


@fixture(scope="package")
def data1():
    return Data(**person1)


@fixture(scope="package")
def data2():
    return Data(**person2)
