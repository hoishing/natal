from natal.enums import AspectType, HouseSystem, Sign, Points, Planet, Asteroid
from natal.house import House
from natal.entity import Entity
import swisseph as swe
from datetime import datetime
import pandas as pd
from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass
from datetime import datetime
from natal.utils import pairs
from natal.aspect import Aspect
from zoneinfo import ZoneInfo  # Add this import
from math import floor

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
    entities: list[Entity] = Field(default_factory=list)

    def __post_init__(self):
        self.set_lat_lon()
        self.set_cusp_asc_mc()
        self.set_entities()

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

    def set_entities(self):
        """Set the positions of the planets and other celestial bodies."""
        bodies = list(Planet) + list(Asteroid) + [p for p in Points if p > 0]

        for body in bodies:
            # return (lat, lon, dist, speed_lat, speed_lon, speed_dist), flag_used)
            # default: flag = swe.FLG_SWIEPH | swe.FLG_SPEED
            (
                (lon, _, _, speed, *_),
                _,
            ) = swe.calc_ut(self.julian_day, body)
            retro = speed < 0
            entity = Entity(body, lon, retro)
            self.entities.append(entity)
            setattr(self, body.name, entity)

    def set_cusp_asc_mc(self) -> None:
        """Calculate the cusps of the houses."""

        cusps, (asc_deg, mc_deg, *_) = swe.houses(
            self.julian_day,
            self.lat,
            self.lon,
            self.house_sys.encode(),
        )
        for i, cusp in enumerate(cusps):
            house = House(num=i + 1, cusp=floor(cusp * 100) / 100)
            self.houses.append(house)
            self.entities.append(Entity(house, cusp))

        asc = Entity(Points.asc, asc_deg)
        mc = Entity(Points.mc, mc_deg)
        self.entities.extend([asc, mc])
        self.asc = asc
        self.mc = mc

    def get_entity(self, body: Planet | Asteroid | Points) -> Entity:
        """Get an entity by body."""
        return next(e for e in self.entities if e.body == body)

    def set_aspects(self):
        """Set the aspects between the planets."""
        entity_pairs = pairs(self.entities)
        for e1, e2 in entity_pairs:
            aspect = Aspect(e1, e2)

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
