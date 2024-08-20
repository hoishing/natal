from natal.enums import AstroEnums, Sign
from typing import NamedTuple


class Position(NamedTuple):
    """position of a astrological entity in natal chart

    Args:
        sign (Sign): zodiac sign of the position
        degree (float): decimal degree of the position

    Example:

        >>> position = Position(Sign.aries, 15.5)
        >>> position.degree
        15.5
        >>> position.dms
        "15° 30'"
    """

    sign: Sign
    """sign of the entity"""
    degree: float
    """decimal degree of the entity"""

    @property
    def dms(self) -> str:
        """Degree Minute Second representation of the position"""
        degrees = int(self.degree)  # Get the whole number part
        minutes = (
            abs(self.degree - degrees) * 60
        )  # Get the decimal part and convert to minutes
        minutes = round(minutes)  # Round minutes to the nearest whole number
        return f"{degrees}° {minutes}'"


class Entity:
    """Astrological entity in `NatalData`"""

    pos: Position

    def __init__(self, entity: AstroEnums) -> None:
        self.entity = entity
