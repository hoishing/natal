from typing import NamedTuple

class AstroObj(NamedTuple):
    name: str
    yr: int
    mo: int
    day: int 
    hr: int 
    min: int 
    lat: float
    lng: float
    house_sys: HouseSys