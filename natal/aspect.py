from typing import NamedTuple
from natal.enums import Entity, Aspect


class Aspect(NamedTuple):
    """Aspect between two astrological entities

    Args:
        entity1 (Entity): first entity
        entity2 (Entity): second entity
        aspect (Aspect): aspect between the entities

    Example:

        >>> aspect = Aspect(entity1, entity2, 120, "trine")
        >>> aspect.aspect
        "trine"
    """

    entity1: Entity
    """first entity"""
    entity2: Entity
    """second entity"""
    aspect: Aspect
    """aspect between the entities"""
