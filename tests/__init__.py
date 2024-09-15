from pytest import fixture
from natal.data import Data
from natal.config import Config

config = Config(
    display={"chiron": True},
)


@fixture(scope="package")
def data():
    return Data(
        name="shing",
        city="hong kong",
        dt="1976-04-20 18:58",
        config=config,
    )
