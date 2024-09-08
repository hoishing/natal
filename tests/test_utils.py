from natal.utils import *
from pytest import fixture


class Foo(DotDict):
    a: str


@fixture(scope="module")
def foo() -> Foo:
    return Foo(a="bar")


def test_dot_notation(foo):
    assert foo.a == "bar"


def test_subscription(foo):
    assert foo["a"] == "bar"


def test_str_to_dt():
    date_str = "1976-04-20 18:58"
    assert str_to_dt(date_str) == datetime(1976, 4, 20, 18, 58)

def test_pairs():
    assert pairs(range(1,5)) == [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
