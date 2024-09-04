"""utility functions for natal"""

from natal.config import Config, load_config
from typing import Iterable


class DotDict(dict):
    # def __init__(self, **kwargs):
    #     self.__dict__.update(kwargs)

    # def __getitem__(self, key):
    #     return getattr(self, key)

    # def __setitem__(self, key, value):
    #     setattr(self, key, value)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)


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


def member_of(const: DotDict, name: str):
    idx: int = const["name"].index(name)
    return {prop: const[prop][idx] for prop in const.__annotations__.keys()}
