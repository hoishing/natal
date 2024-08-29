from pydantic import BaseModel, Field
from natal.enums import Sign


class House(BaseModel):
    num: int = Field(ge=1, le=12)
    cusp: float = Field(ge=0, lt=360)

    @property
    def sign(self) -> Sign:
        """sign of the house"""
        return Sign(self.num)
