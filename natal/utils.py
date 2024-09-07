"""utility functions for natal"""

from pydantic import BaseModel
from natal.config import Config, load_config
from typing import Iterable
from collections.abc import Mapping


class BaseDict(BaseModel, Mapping):
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __iter__(self):
        return iter(self.model_fields)

    def __len__(self):
        return len(self.model_fields)


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
