from natal.config import load_config
from tempfile import NamedTemporaryFile
from pytest import fixture
from typing import Generator

config = """
light_theme:
    red: "#ff0000"
    yellow: "#ffff00"
    green: "#00ff00"
    blue: "#0000ff"
    aqua: "#00ffff"


display:
    mean_node: False
    chiron: True

orb:
    conjunction: 8
    opposition: 7
    trine: 6
    square: 6
    sextile: 8
"""


# create a fixture that creates a temporary file with the config
@fixture
def tmp_config_file() -> Generator[str, None, None]:
    with NamedTemporaryFile(mode="w") as f:
        f.write(config)
        f.flush()
        yield f.name


# test the load_config function by using the fixture
def test_load_config(tmp_config_file: str) -> None:
    cfg = load_config(tmp_config_file)

    assert cfg.light_theme.red == "#ff0000"
    assert cfg.display.mean_node == False
    assert cfg.orb.opposition == 7
