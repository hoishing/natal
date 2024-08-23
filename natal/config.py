"""package configuration module

- load natal.yml config file if exists
- provide default configuration if natal.yml does not exist
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
    sextile: int = 5


class Config(BaseModel):
    """package configuration model"""

    orb: Orb


def load_config() -> Config:
    """load `natal.yml` file, otherwise return default configuration"""
    if Path("natal.yml").exists():
        with open("natal.yml") as f:
            py_dict = yaml.safe_load(f)
            return Config(**py_dict)

    return Config(orb=Orb())


if "__main__" == __name__:
    import json

    schema = Config.model_json_schema()
    with open("natal/data/natal_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
