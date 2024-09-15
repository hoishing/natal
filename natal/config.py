"""package configuration module

- load natal_config.yml config file if exists
- provide default config file does not exist
- generate json schema for the configuration
"""

import yaml
from pydantic import BaseModel
from typing import Any, Mapping, Iterator
from pathlib import Path
from io import IOBase


class ModelDict(BaseModel, Mapping):
    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)


class Orb(ModelDict):
    """aspect orb model with default values"""

    conjunction: int = 8
    opposition: int = 7
    trine: int = 6
    square: int = 6
    sextile: int = 5


class Theme(ModelDict):
    """default colors"""

    fire: str = "#ef476f"  # fire, square, Asc
    earth: str = "#ffd166"  # earth, MC
    air: str = "#06d6a0"  # air, trine
    water: str = "#81bce7"  # water, opposition
    points: str = "#118ab2"  # lunar nodes, sextile
    asteroids: str = "#AA96DA"  # asteroids
    positive: str = "#FFC0CB"  # positive
    negative: str = "#AD8B73"  # negative
    others: str = "#FFA500"  # conjunction
    foreground: str
    background: str
    transparency: float


class LightTheme(Theme):
    """default light colors"""

    foreground: str = "#758492"
    background: str = "#F7F5E6"
    transparency: float = 0.1


class DarkTheme(Theme):
    """default dark colors"""

    foreground: str = "#F7F3F0"
    background: str = "#343a40"
    transparency: float = 0.1


class Display(ModelDict):
    """display the celestial bodies or not"""

    sun: bool = True
    moon: bool = True
    mercury: bool = True
    venus: bool = True
    mars: bool = True
    jupiter: bool = True
    saturn: bool = True
    uranus: bool = True
    neptune: bool = True
    pluto: bool = True
    mean_node: bool = True
    # true_node: bool = False
    # mean_apog: bool = False
    # oscu_apog: bool = False
    # earth: bool = False
    chiron: bool = False
    # pholus: bool = False
    # ceres: bool = False
    # pallas: bool = False
    # juno: bool = False
    # vesta: bool = False
    asc: bool = True
    ic: bool = False
    dsc: bool = False
    mc: bool = True


class ChartOptions(ModelDict):
    """chart configuration"""

    stroke_width: int = 1
    stroke_opacity: float = 1
    font: str = "Arial Unicode MS, sans-serif"
    font_size_fraction: float = 0.55
    inner_min_degree: float = 6
    outer_min_degree: float = 7
    margin_factor: float = 0.1


class Config(ModelDict):
    """package configuration model"""

    is_light_theme: bool = False
    orb: Orb = Orb()
    light_theme: LightTheme = LightTheme()
    dark_theme: DarkTheme = DarkTheme()
    display: Display = Display()
    chart: ChartOptions = ChartOptions()

    @property
    def theme(self) -> Theme:
        """return light or dark theme colors"""
        return self.light_theme if self.is_light_theme else self.dark_theme


def load_config(file: str | Path | IOBase = "natal_config.yml") -> Config:
    """load configuration file"""
    if isinstance(file, IOBase):
        obj = yaml.safe_load(file)
        return Config(**obj)

    path = Path(file)
    if not path.exists():
        return Config()

    with open(path, "r") as f:
        obj = yaml.safe_load(f)
        return Config(**obj)


if "__main__" == __name__:
    import json

    schema = Config.model_json_schema()
    with open("natal/data/natal_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
