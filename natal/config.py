"""
package configuration module

- Load natal_config.yml config file if exists.
- Provide default config file if it does not exist.
- Generate JSON schema for the configuration.
"""

import yaml
from darkdetect import isDark
from io import IOBase
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Iterator, Literal, Mapping

ThemeType = Literal["auto", "light", "dark", "mono"]


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
    """default orb for natal chart"""

    conjunction: int = 7
    opposition: int = 6
    trine: int = 6
    square: int = 6
    sextile: int = 5


class Theme(ModelDict):
    """
    Default colors for the chart.
    """

    fire: str = "#ef476f"  # fire, square, Asc
    earth: str = "#ffd166"  # earth, MC
    air: str = "#06d6a0"  # air, trine
    water: str = "#81bce7"  # water, opposition
    points: str = "#118ab2"  # lunar nodes, sextile
    asteroids: str = "#AA96DA"  # asteroids
    positive: str = "#FFC0CB"  # positive
    negative: str = "#AD8B73"  # negative
    others: str = "#FFA500"  # conjunction
    transparency: float = 0.1
    foreground: str
    background: str
    dim: str


class LightTheme(Theme):
    """
    Default light colors.
    """

    foreground: str = "#758492"
    background: str = "#FFFDF1"
    dim: str = "#A4BACD"


class DarkTheme(Theme):
    """
    Default dark colors.
    """

    foreground: str = "#F7F3F0"
    background: str = "#343a40"
    dim: str = "#515860"


class Display(ModelDict):
    """
    Display settings for celestial bodies.
    """

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
    chiron: bool = False
    pholus: bool = False
    ceres: bool = False
    pallas: bool = False
    juno: bool = False
    vesta: bool = False
    asc: bool = True
    ic: bool = False
    dsc: bool = False
    mc: bool = True


class Chart(ModelDict):
    """
    Chart configuration settings.
    """

    stroke_width: int = 1
    stroke_opacity: float = 1
    font: str = "Arial Unicode MS, sans-serif"
    font_size_fraction: float = 0.55
    inner_min_degree: float = 9
    outer_min_degree: float = 7
    margin_factor: float = 0.1
    ring_thickness_fraction: float = 0.15


class Config(ModelDict):
    """
    Package configuration model.
    """

    theme_type: ThemeType = "auto"
    orb: Orb = Orb()
    light_theme: LightTheme = LightTheme()
    dark_theme: DarkTheme = DarkTheme()
    display: Display = Display()
    chart: Chart = Chart()

    @property
    def theme(self) -> Theme:
        """
        Return theme colors based on the theme type.

        Returns:
            Theme: The theme colors.
        """
        match self.theme_type:
            case "light":
                return self.light_theme
            case "dark":
                return self.dark_theme
            case "mono":
                kwargs = {key: "#888888" for key in self.light_theme.model_dump()}
                kwargs["background"] = "white"
                kwargs["transparency"] = 0
                return Theme(**kwargs)
            case "auto":
                return self.dark_theme if isDark() else self.light_theme


def load_config(file: str | Path | IOBase = "natal_config.yml") -> Config:
    """
    Load configuration file.

    Args:
        file (str | Path | IOBase): The configuration file path or file object.

    Returns:
        Config: The loaded configuration.
    """
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

    # generate json schema for the config file
    schema = Config.model_json_schema()
    with open("natal/data/natal_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
