import pandas as pd
import swisseph as swe
from datetime import datetime
from math import floor
from natal.classes import Aspect, Body, HouseSys, MovableBody, Sign, House, SignMember
from natal.config import load_config
from natal.const import *
from natal.utils import pairs, member_of
from pydantic import Field, field_validator, BaseModel
from zoneinfo import ZoneInfo
from typing import Any

swe.set_ephe_path("natal/data")
CONFIG = load_config()


class Data(BaseModel):
    """Data object for a natal chart."""

    name: str
    city: str
    dt: datetime
    lat: float = Field(None, ge=-90, le=90)
    lon: float = Field(None, ge=-180, le=180)
    timezone: str = ""
    house_sys: HouseSys = HouseSys.Placidus
    houses: list[House] = []
    planets: list[MovableBody] = []
    extras: list[MovableBody] = []
    signs: list[Sign] = []
    aspectable: list[MovableBody] = []
    aspects: list[Aspect] = []
    body_houses: dict[str, int] = {}

    class Config:
        extra = "allow"

    def model_post_init(self, __context: Any) -> None:
        self.set_lat_lon()
        self.set_houses_asc_mc()
        self.set_movable_bodies()
        self.aspectable = self.planets + self.extras + [self.asc, self.mc]
        self.set_signs()
        self.set_aspects()
        self.set_body_houses()
        self.set_rulers()

    @field_validator("dt")
    @classmethod
    def check_year(cls, dt):
        if not (1800 <= dt.year <= 2399):
            raise ValueError("Year must be between 1800 and 2399")
        return dt

    @property
    def julian_day(self) -> float:
        # Convert dt to UTC
        local_tz = ZoneInfo(self.timezone)
        local_dt = self.dt.replace(tzinfo=local_tz)
        utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
        return swe.date_conversion(
            utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60
        )[1]

    def set_lat_lon(self):
        """set the geographical information of a city."""

        # fields: name, ascii_name, pop, timezone, country, lat, lon
        cities = pd.read_csv("natal/data/cities.csv")
        info = cities[cities["ascii_name"].str.lower() == self.city.lower()].iloc[0]
        self.lat = float(info["lat"])
        self.lon = float(info["lon"])
        self.timezone = info["timezone"]

    def set_movable_bodies(self):
        """Set the positions of the planets and other celestial bodies."""

        self.planets = self.set_positions(PlanetName.__args__, PLANETS)
        self.extras = self.set_positions(ExtraName.__args__, EXTRAS)

    def set_houses_asc_mc(self) -> None:
        """Calculate the cusps of the houses."""

        cusps, (asc_deg, mc_deg, *_) = swe.houses(
            self.julian_day,
            self.lat,
            self.lon,
            self.house_sys.encode(),
        )

        for i, cusp in enumerate(cusps):
            cusp = floor(cusp * 100) / 100
            name = HouseName.__args__[i]
            house = MovableBody(
                name=name,
                value=i + 1,
                symbol=HOUSES["symbol"][i],
                color=HOUSES["color"][i],
                degree=cusp,
            )
            self.houses.append(house)

        self.asc = MovableBody(
            name="asc", symbol="Asc", value=-2, color="fire", degree=asc_deg
        )
        self.mc = MovableBody(
            name="mc", symbol="MC", value=-3, color="earth", degree=mc_deg
        )

    def set_signs(self):
        """Set the signs of the zodiac."""
        for i, name in enumerate(SignName.__args__):
            pos = Sign(
                name=name,
                value=i + 1,
                symbol=SIGNS["symbol"][i],
                color=SIGNS["color"][i],
                degree=(i * 30 + (360 - self.asc.degree)) % 360,
                ruler=SIGNS["ruler"][i],
                quality=SIGNS["quality"][i],
                element=SIGNS["element"][i],
                polarity=SIGNS["polarity"][i],
            )
            setattr(self, name, pos)
            self.signs.append(pos)

    def set_aspects(self):
        """Set the aspects between the planets."""
        body_pairs = pairs(self.aspectable)
        for e1, e2 in body_pairs:
            angle = abs(e1.degree - e2.degree)
            for i, asp_name in enumerate(AspectName.__args__):
                max_orb = ASPECTS["value"][i] + CONFIG.orb[asp_name]
                min_orb = ASPECTS["value"][i] - CONFIG.orb[asp_name]
                if min_orb <= angle <= max_orb:
                    aspect_type = Body(
                        name=asp_name,
                        symbol=ASPECTS["symbol"][i],
                        value=ASPECTS["value"][i],
                        color=ASPECTS["color"][i],
                    )
                    self.aspects.append(Aspect(e1, e2, aspect_type, None, None))

    def set_body_houses(self):
        """Set the houses of the bodies."""
        for body in self.aspectable:
            house = self.house_of(body)
            self.body_houses[body.name] = house

    def set_rulers(self):
        houses = []
        for house in self.houses:
            ruler_obj = getattr(self, house.sign.ruler)
            ruled_house = House(
                **house.model_dump(),
                ruler=ruler_obj.name,
                ruler_sign=f"{ruler_obj.sign.symbol} {ruler_obj.sign.name}",
                ruler_house=self.body_houses[ruler_obj.name],
            )
            setattr(self, house.name, ruled_house)
            houses.append(ruled_house)
        self.houses = houses

    def __str__(self):
        op = ""
        op += f"Name: {self.name}\n"
        op += f"City: {self.city}\n"
        op += f"Date: {self.dt}\n"
        op += f"Latitude: {self.lat}\n"
        op += f"Longitude: {self.lon}\n"
        op += f"House System: {self.house_sys}\n"
        op += "Planets:\n"
        for e in self.planets:
            op += f"{e.name}: {e.signed_dms}\n"
        op += "Extras:\n"
        for e in self.extras:
            op += f"{e.name}: {e.signed_dms}\n"
        op += f"Asc: {self.asc.signed_dms}\n"
        op += f"MC: {self.mc.signed_dms}\n"
        op += "Houses:\n"
        for e in self.houses:
            op += f"{e.name}: {e.signed_dms}\n"
        op += "Signs:\n"
        for e in self.signs:
            op += f"{e.name}: degree={e.degree:.2f}, ruler={e.ruler}, color={e.color}, quality={e.quality}, element={e.element}, polarity={e.polarity}\n"
        op += "Aspects:\n"
        for e in self.aspects:
            op += f"{e.body1.name} {e.aspect_type.symbol} {e.body2.name}: {e.aspect_type.color}\n"
        return op

    # utils ===============================

    def get_degree(self, swe_const: int) -> tuple[float, bool]:
        ((lon, _, _, speed, *_), _) = swe.calc_ut(self.julian_day, swe_const)
        retro = speed < 0
        return lon, retro

    def set_positions(self, names: list[str], const: dict) -> list[MovableBody]:
        """Set the positions of the planets and other celestial bodies."""
        output = []
        for i, name in enumerate(names):
            value = const["value"][i]
            degree, retro = self.get_degree(value)
            pos = MovableBody(
                name=name,
                value=value,
                symbol=const["symbol"][i],
                color=const["color"][i],
                degree=degree,
                retro=retro,
            )
            setattr(self, name, pos)
            output.append(pos)
        return output

    def house_of(self, body: MovableBody) -> int:
        """House of the body."""
        sorted_houses = sorted(self.houses, key=lambda x: x.degree, reverse=True)
        for house in sorted_houses:
            if body.degree >= house.degree:
                return house.value
        return sorted_houses[0].value

    def ruler_of(self, house: MovableBody) -> str:
        """Ruler of the house."""
        return getattr(self, house.ruler)
