from natal.entity import Entity
from natal.config import load_config


class Aspect(Entity):
    name: str
    symbol: str
    color: str

    @property
    def angle(self) -> int:
        return dict(
            conjunction=0,
            opposition=180,
            trine=120,
            square=90,
            sextile=60,
        )[self.name]

    @property
    def orb(self) -> float:
        return getattr(load_config().orb, self.name)

    @property
    def max(self) -> float:
        return self.angle + self.orb

    @property
    def min(self) -> float:
        return self.angle - self.orb
