from pydantic.dataclasses import dataclass
from pydantic import Field

from natal.enums import Sign, HouseType


@dataclass
class House:
    """House in natal chart"""

    num: int = Field(ge=1, le=12, alias="name")
    cusp: float = Field(ge=0, lt=360)

    @property
    def name(self) -> str:
        """name of the house"""
        return str(self.num)

    @property
    def sign(self) -> Sign:
        """sign of the house"""
        return Sign(self.num)

    @property
    def body(self) -> HouseType:
        """type of the house"""
        return HouseType(self.num)

    

