import pandas as pd
import swisseph as swe
from datetime import datetime
from math import floor
from natal.classes import (
    Aspect,
    Aspectable,
    Body,
    Extra,
    House,
    HouseSys,
    HouseWithRuler,
    Planet,
    Sign,
)
from natal.config import load_config
from natal.const import *
from natal.utils import pairs, str_to_dt
from zoneinfo import ZoneInfo

swe.set_ephe_path("natal/data")
CONFIG = load_config()


class Data(DotDict):
    """Data object for a natal chart"""

    name: str
    city: str
    dt: datetime | str
    lat: float = None
    lon: float = None
    timezone: str = None
    house_sys: HouseSys = HouseSys.Placidus
    houses: list[House] = []
    planets: list[Planet] = []
    extras: list[Extra] = []
    signs: list[Sign] = []
    aspectable: list[Aspectable] = []
    aspects: list[Aspect] = []

    def __init__(self, name: str, city: str, dt: datetime | str):
        self.name = name
        self.city = city
        if isinstance(dt, str):
            dt = str_to_dt(dt)
        self.dt = dt
        self.set_lat_lon()
        self.set_houses_asc_mc()
        self.set_movable_bodies()
        self.aspectable = self.planets + self.extras + [self.asc, self.mc]
        self.set_signs()
        self.set_aspects()
        self.set_rulers()

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

        self.planets = self.set_positions(PLANET_MEMBERS)
        self.extras = self.set_positions([m for m in EXTRA_MEMBERS if m.value > 0])

    def set_houses_asc_mc(self) -> None:
        """Calculate the cusps of the houses."""

        cusps, (asc_deg, mc_deg, *_) = swe.houses(
            self.julian_day,
            self.lat,
            self.lon,
            self.house_sys.encode(),
        )

        for house, cusp in zip(HOUSE_MEMBERS, cusps):
            house_body = House(
                **house,
                degree=floor(cusp * 100) / 100,
            )
            self.houses.append(house_body)

        self.asc = Extra(
            name="asc", symbol="Asc", value=-2, color="fire", degree=asc_deg
        )
        self.mc = Extra(name="mc", symbol="MC", value=-3, color="earth", degree=mc_deg)

    def set_signs(self):
        """Set the signs of the zodiac."""
        for i, sign_member in enumerate(SIGN_MEMBERS):
            sign = Sign(
                **sign_member,
                degree=(i * 30 + (360 - self.asc.degree)) % 360,
            )
            setattr(self, sign.name, sign)
            self.signs.append(sign)

    def set_aspects(self):
        """Set the aspects between the planets."""
        body_pairs = pairs(self.aspectable)
        for b1, b2 in body_pairs:
            ordered = sorted([b1, b2], key=lambda x: x.degree)
            org_angle = ordered[1].degree - ordered[0].degree
            angle = (
                360 - org_angle if org_angle > 180 else org_angle
            )  # get the smaller angle
            for aspect_member in ASPECT_MEMBERS:
                max_orb = aspect_member.value + CONFIG.orb[aspect_member.name]
                min_orb = aspect_member.value - CONFIG.orb[aspect_member.name]
                if min_orb <= angle <= max_orb:
                    # decreasing angle approach aspect
                    applying = ordered[0].speed > ordered[1].speed
                    if angle < aspect_member.value:
                        applying = not applying  # increasing angle approach aspect
                    # reverse if org_angle is reflex angle
                    applying = not applying if org_angle > 180 else applying
                    self.aspects.append(
                        Aspect(
                            body1=b1,
                            body2=b2,
                            aspect_member=aspect_member,
                            applying=applying,
                            orb=abs(angle - aspect_member.value),
                        )
                    )

    def set_rulers(self):
        houses = []
        for house in self.houses:
            ruler = getattr(self, house.sign.ruler)
            classic_ruler = getattr(self, house.sign.classic_ruler)
            ruled_house = HouseWithRuler(
                **house,
                ruler=ruler.name,
                ruler_sign=f"{ruler.sign.symbol} {ruler.sign.name}",
                ruler_house=self.house_of(ruler.name),
                classic_ruler=classic_ruler.name,
                classic_ruler_sign=f"{classic_ruler.sign.symbol} {classic_ruler.sign.name}",
                classic_ruler_house=self.house_of(classic_ruler.name),
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
            op += f"{e.body1.name} {e.aspect_member.symbol} {e.body2.name}: {e.aspect_member.color}\n"
        return op

    # utils ===============================

    def set_positions(self, members: list[Body]) -> list[Aspectable]:
        """Set the positions of the planets and other celestial bodies."""
        output = []
        for member in members:
            ((lon, _, _, speed, *_), _) = swe.calc_ut(self.julian_day, member.value)
            pos = Aspectable(
                **member,
                degree=lon,
                speed=speed,
            )
            setattr(self, member.name, pos)
            output.append(pos)
        return output

    def house_of(self, body_name: str) -> int:
        """House of a celestial body."""
        body = getattr(self, body_name)
        sorted_houses = sorted(self.houses, key=lambda x: x.degree, reverse=True)
        for house in sorted_houses:
            if body.degree >= house.degree:
                return house.value
        return sorted_houses[0].value
