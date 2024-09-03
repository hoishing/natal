import csv
from pydantic.dataclasses import dataclass

@dataclass
class Entity:
    """basic entity in natal chart"""

    name: str
    symbol: str
    color: str


ENTITIES: list[Entity] = []


with open("natal/data/entities.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        ENTITIES.append(Entity(**row))