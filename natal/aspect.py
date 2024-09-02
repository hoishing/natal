from typing import NamedTuple
from natal.enums import AspectType, Points, Asteroid, Planet
from natal.config import load_config, Config


class Aspect(NamedTuple):
    """Aspect between two astrological entities

    Args:
        entity1 (Planet | Points | Asteroid): first entity
        entity2 (Planet | Points | Asteroid): second entity
        aspect (AspectEnum): aspect between the entities

    Example:

        >>> aspect = Aspect(entity1, entity2, 120, "trine")
        >>> aspect.aspect
        "trine"
    """

    entity1: Planet | Points | Asteroid
    """first entity"""
    entity2: Planet | Points | Asteroid
    """second entity"""
    aspect: AspectType
    """aspect between the entities"""

    @property
    def config(self) -> Config:
        """config"""
        return load_config()

    @property
    def orb(self) -> int:
        """orb of the aspect"""
        return getattr(self.config.orb, self.aspect.name)
