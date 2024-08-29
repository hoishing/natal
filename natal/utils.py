"""utility functions for natal"""
from natal.config import Config, load_config

def color_hex(name: str, config: Config = load_config()) -> str:
    """get color hex from name and Config instance, default to 'nata_config.yml'"""
    return getattr(config.colors, name)