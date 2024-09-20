from natal.config import load_config, Config
from tempfile import NamedTemporaryFile
from pytest import fixture
from typing import Generator
from io import StringIO

config = """
light_theme:
    fire: "#ff0000"
    earth: "#ffff00"
    air: "#00ff00"
    water: "#0000ff"
    points: "#00ffff"


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
def test_load_config_from_path(tmp_config_file: str) -> None:
    cfg = load_config(tmp_config_file)

    assert cfg.light_theme.fire == "#ff0000"
    assert cfg.display.mean_node == False
    assert cfg.orb.opposition == 7


def test_load_config_from_io() -> None:
    file = StringIO(config)
    cfg = load_config(file)
    assert cfg.light_theme.fire == "#ff0000"
    assert cfg.display.mean_node == False
    assert cfg.orb.opposition == 7


def test_mono_theme() -> None:
    cfg = Config(**dict(theme_type="mono"))
    assert cfg.theme_type == "mono"
    assert cfg.theme.foreground == cfg.theme.fire
    assert cfg.theme.background == "white"
    assert cfg.theme.transparency == 0
