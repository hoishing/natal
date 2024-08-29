from dataclasses import dataclass
from typing import Any
from natal.enums import Aspect, HouseSystem, Sign, Points, Planet, Asteroid
from natal.entity import Entity
import swisseph as swe
from datetime import datetime
import pandas as pd
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

swe.set_ephe_path("natal/data")


@dataclass
class Natal(BaseModel):
    """Data object for a natal chart."""

    name: str
    city: str
    dt: datetime
    hse_sys: HouseSystem = HouseSystem.Placidus
    entities: list[Entity] = []
    cusps: list[float] = []

    def model_post_init(self) -> None:
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
        return swe.date_conversion(
            self.dt.year, self.dt.month, self.dt.day, self.dt.hour + self.dt.minute / 60
        )[1]

    def set_lat_lon(self):
        """set the geographical information of a city."""

        # fields: name, ascii_name, pop, timezone, country, lat, lon
        cities = pd.read_csv("natal/data/cities.csv")
        info = cities[cities["ascii_name"] == self.city].iloc[0]
        self.lat = info["lat"]
        self.lon = info["lon"]

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
            self.entities.append(Entity(body, lon, retro))

    def set_cusp_asc_mc(self) -> None:
        """Calculate the cusps of the houses."""

        self.cusp, (asc_deg, mc_deg, *_) = swe.houses(
            self.julian_day,
            self.lat,
            self.lon,
            self.hse_sys.encode(),
        )
        self.entities.append(Entity(Points.asc, asc_deg))
        self.entities.append(Entity(Points.mc, mc_deg))
