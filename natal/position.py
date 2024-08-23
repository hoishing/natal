from natal.enums import Sign, Entity
from typing import NamedTuple


class Position(NamedTuple):
    """position of a astrological entity in natal chart

    Args:
        entity (AstroEnums): astrological entity of the position
        sign (Sign): zodiac sign of the position
        degree (float): decimal degree of the position

    Example:

        >>> position = Position(Planet.moon, Sign.aries, 15.5)
        >>> position.degree
        15.5
        >>> position.dms
        "15° 30'"
    """

    entity: Entity
    """astrological entity of the position"""

    sign: Sign
    """sign of the entity"""

    degree: float
    """decimal degree of the entity, between 0 and 29.99"""

    @property
    def dms(self) -> str:
        """Degree Minute Second representation of the position"""
        degrees = int(self.degree)  # Get the whole number part
        minutes = (
            abs(self.degree - degrees) * 60
        )  # Get the decimal part and convert to minutes
        minutes = round(minutes)  # Round minutes to the nearest whole number
        return f"{degrees}° {minutes}'"
