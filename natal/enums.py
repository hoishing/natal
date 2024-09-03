from enum import StrEnum


class HouseSystem(StrEnum):
    """Astrological house systems, values are Swiss Ephemeris constants"""

    Placidus = "P"
    Koch = "K"
    Porphyry = "O"
    Regiomontanus = "R"
    Campanus = "C"
    Equal = "E"
    Whole_Sign = "W"
