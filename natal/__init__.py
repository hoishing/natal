from pydantic.dataclasses import dataclass
from pydantic import Field, field_validator
from datetime import datetime
from zoneinfo import ZoneInfo
import swisseph as swe
import pandas as pd
from abc import ABC, abstractmethod
from typing import NamedTuple

class Entity(NamedTuple):
    name: str
    color: str
    symbol: str




@dataclass
class Natal:
    name: str
    city: str
    dt: datetime
    lat: float = Field(None, ge=-90, le=90)
    lon: float = Field(None, ge=-180, le=180)

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

        pla