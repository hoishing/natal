from pytest import fixture
from natal.data import Data
from natal.config import Config

config = Config(
    display={"chiron": True, "mean_node": True},
    orb={"conjunction": 8, "opposition": 7, "trine": 6, "square": 6, "sextile": 5},
)


@fixture(scope="package")
def data():
    return Data(
        name="shing",
        city="hong kong",
        dt="1976-04-20 18:58",
        config=config,
    )
