from natal.enums import HouseSystem
from natal.entity import Position
import swisseph as swe
from datetime import datetime
import pandas as pd
from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass
from datetime import datetime
from natal.utils import pairs
from zoneinfo import ZoneInfo
from math import floor
from natal.aspect import Aspect
from natal.const import ENTITIES

swe.set_ephe_path("natal/data")


@dataclass
class NatalData:
    """Data object for a natal chart."""

    name: str
    city: str
    dt: datetime
    lat: float = Field(None, ge=-90, le=90)
    lon: float = Field(None, ge=-180, le=180)
    house_sys: HouseSystem = HouseSystem.Placidus
    aspects: list[Aspect] = Field(default_factory=list)


    def __post_init__(self):
        self.set_lat_lon()
        for entity in ENTITIES:
            setattr(self, entity.name, entity)
        self.set_cusp_asc_mc()
        self.set_signs()
        self.set_movable_entities()

    @field_validator("dt")
    @classmethod
    def check_year(cls, dt):
        if not (1800 <= dt.year <= 2399):
            raise ValueError("Year must be between 1800 and 2399")
        return dt

    @property
    def julian_day(self) -> float:
        # Convert dt to UTC
        local_tz = ZoneInfo(self.city_timezone)
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
        self.city_timezone = info["timezone"]  # Add this line to get the timezone

    def set_movable_entities(self):
        """Set the positions of the planets and other celestial bodies."""

        self.planets = [
            self.sun,
            self.moon,
            self.mercury,
            self.venus,
            self.mars,
            self.jupiter,
            self.saturn,
            self.uranus,
            self.neptune,
            self.pluto,
        ]

        self.others = [
            self.chiron,
            self.pholus,
            self.ceres,
            self.pallas,
            self.juno,
            self.vesta,
            self.mean_node,
        ]

        entities: list[Entity] = self.planets + self.others

        for entity in entities:
            # return (lat, lon, dist, speed_lat, speed_lon, speed_dist), flag_used)
            # default: flag = swe.FLG_SWIEPH | swe.FLG_SPEED
            ((lon, _, _, speed, *_), _) = swe.calc_ut(
                self.julian_day, getattr(swe, entity.name)
            )
            movable_entity = Position.create(entity)
            movable_entity.degree = lon
            movable_entity.retro = speed < 0
            setattr(self, entity.name, movable_entity)

    def set_cusp_asc_mc(self) -> None:
        """Calculate the cusps of the houses."""

        self.houses = [
            self.one,
            self.two,
            self.three,
            self.four,
            self.five,
            self.six,
            self.seven,
            self.eight,
            self.nine,
            self.ten,
            self.eleven,
            self.twelve,
        ]

        cusps, (asc_deg, mc_deg, *_) = swe.houses(
            self.julian_day,
            self.lat,
            self.lon,
            self.house_sys.encode(),
        )

        for i, house in enumerate(self.houses):
            movable_house = Position.create(house)
            movable_house.degree = floor(cusps[i] * 100) / 100
            setattr(self, house.name, movable_house)

        asc = Position.create(self.asc)
        asc.degree = round(asc_deg, 2)
        mc = Position.create(self.mc)
        mc.degree = round(mc_deg, 2)
        self.asc = asc
        self.mc = mc

    def set_signs(self):
        """Set the signs of the entities."""
        self.signs = [
            self.aries,
            self.taurus,
            self.gemini,
            self.cancer,
            self.leo,
            self.virgo,
            self.libra,
            self.scorpio,
            self.sagittarius,
            self.capricorn,
            self.aquarius,
            self.pisces,
        ]
        for i, sign in enumerate(self.signs):
            sign.degree = ((i * 30) + self.asc.degree) % 360

    def set_aspects(self):
        """Set the aspects between the planets."""

        self.aspect_entities = [
            self.conjunction,
            self.opposition,
            self.trine,
            self.square,
            self.sextile,
        ]

        bodies = self.planets + self.others + [self.asc, self.mc]
        entity_pairs = pairs(bodies)
        for e1, e2 in entity_pairs:
            for asp in self.aspect_entities:
                aspect = Aspect(asp.name, asp.symbol, asp.color)
                angle = abs(e1.degree - e2.degree)
                if aspect.min <= angle <= aspect.max:
                    aspect = (e1, e2, aspect)
                    self.aspects.append(aspect)

    def __str__(self):
        op = ""
        op += f"Name: {self.name}\n"
        op += f"City: {self.city}\n"
        op += f"Date: {self.dt}\n"
        op += f"Latitude: {self.lat}\n"
        op += f"Longitude: {self.lon}\n"
        op += f"House System: {self.house_sys}\n"
        op += f"Entities:\n"
        for e in self.entities:
            op += f"{e.body.name}: {e.signed_dms}\n"
        return op
