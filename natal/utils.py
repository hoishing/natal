"""utility functions for natal"""
from natal.config import Config, load_config
from typing import Iterable


def color_hex(name: str, config: Config = load_config()) -> str:
    """get color hex from name and Config instance, default to 'nata_config.yml'"""
    return getattr(config.colors, name)


def pairs(iterable: Iterable) -> list[tuple]:
    """pairs of iterable"""
    output = []
    for i in range(len(iterable)):
        for j in range(i + 1, len(iterable)):
            output.append((iterable[i], iterable[j]))
    return output
