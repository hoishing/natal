from typing import NamedTuple
from natal.enums import Body, Aspect, House
from natal.config import CONFIG


class Aspect(NamedTuple):
    """Aspect between two astrological entities

    Args:
        entity1 (Planet | House): first entity
        entity2 (Planet | House): second entity
        aspect (Aspect): aspect between the entities

    Example:

        >>> aspect = Aspect(entity1, entity2, 120, "trine")
        >>> aspect.aspect
        "trine"
    """

    entity1: Body | House
    """first entity"""
    entity2: Body | House
    """second entity"""
    enum: Aspect
    """aspect between the entities"""

    @property
    def orb(self) -> int:
        """orb of the aspect"""
        return getattr(CONFIG.orb, self.enum.name)
