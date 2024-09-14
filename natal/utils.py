"""utility functions for natal"""

from natal.config import Config, load_config
from typing import Iterable, Any, Mapping
from datetime import datetime
from types import SimpleNamespace

class DotDict(SimpleNamespace, Mapping):
    # def __init__(self, /, **kwargs):
    #     self.__dict__.update(kwargs)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __iter__(self):
        return iter(self.__dict__.keys())

    def __len__(self):
        return len(self.__dict__)


def color_hex(name: str, config: Config = load_config()) -> str:
    """get color hex from name and Config instance, default to 'nata_config.yml'"""
    return getattr(config.colors, name)


def pairs[T](iterable: Iterable[T]) -> list[tuple[T, T]]:
    """pairs of iterable"""
    output = []
    for i in range(len(iterable)):
        for j in range(i + 1, len(iterable)):
            output.append((iterable[i], iterable[j]))
    return output


def member_of[T](const: list[T], name: str) -> T:
    idx: int = const["name"].index(name)
    return {prop: const[prop][idx] for prop in const.model_fields}


def str_to_dt(dt_str: str) -> datetime:
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
