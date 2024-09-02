"""package configuration module

- load natal_config.yml config file if exists
- provide default config file does not exist
- generate json schema for the configuration
"""

import yaml
from pydantic import BaseModel
from pathlib import Path


class Orb(BaseModel):
    """aspect orb model with default values"""

    conjunction: int = 8
    opposition: int = 8
    trine: int = 6
    square: int = 6
    sextile: int = 4


class Theme(BaseModel):
    """default colors"""

    fire: str = "#ef476f"  # fire, square, Asc
    earth: str = "#ffd166"  # earth, MC
    air: str = "#06d6a0"  # air, trine
    water: str = "#81bce7"  # water, opposition
    points: str = "#118ab2"  # lunar nodes, sextile
    asteroids: str = "##AA96DA"  # asteroids
    positive: str = "#FFC0CB"  # positive
    negative: str = "#AD8B73"  # negative
    others: str = "#FFA500"  # conjunction
    foreground: str
    background: str


class LightTheme(Theme):
    """default light colors"""

    foreground: str = "#343a40"
    background: str = "#F7F3F0"


class DarkTheme(Theme):
    """default dark colors"""

    foreground: str = "#F7F3F0"
    background: str = "#343a40"


class Display(BaseModel):
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
    true_node: bool = False
    mean_apog: bool = False
    oscu_apog: bool = False
    earth: bool = False
    chiron: bool = False
    pholus: bool = False
    ceres: bool = False
    pallas: bool = False
    juno: bool = False
    vesta: bool = False
    asc: bool = True
    mc: bool = True


class Config(BaseModel):
    """package configuration model"""

    is_light_theme: bool = True
    orb: Orb = Orb()
    light_theme: LightTheme = LightTheme()
    dark_theme: DarkTheme = DarkTheme()
    display: Display = Display()

    @property
    def theme(self) -> Theme:
        """return light or dark theme colors"""
        return self.light_theme if self.is_light_theme else self.dark_theme


def load_config(file: str = "natal_config.yml") -> Config:
    """load configuration file

    Test:
        tests/test_config.py
    """
    config = Path(file)
    if not config.exists():
        return Config()
    with open(file) as f:
        obj = yaml.safe_load(f)
    return Config(**obj)


if "__main__" == __name__:
    import json

    schema = Config.model_json_schema()
    with open("natal/data/natal_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
