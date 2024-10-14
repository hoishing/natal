import itertools
from pathlib import Path
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
    Planet,
    Sign,
    Vertex,
)
from natal.config import Config, load_config
from natal.const import *
from natal.utils import pairs, str_to_dt
from typing import Iterable, Self
from zoneinfo import ZoneInfo

type BodyPairs = Iterable[tuple[Aspectable, Aspectable]]

data_folder = Path(__file__).parent.absolute() / "sweph"
swe.set_ephe_path(str(data_folder))


class Data(DotDict):
    """
    Data object for a natal chart.
    """

    cities = pd.read_csv(data_folder / "cities.csv.gz")

    def __init__(
        self,
        name: str,
        city: str,
        dt: datetime | str,
        house_sys: HouseSys = HouseSys.Placidus,
        config: Config = load_config(),
    ):
        self.name = name
        self.city = city
        if isinstance(dt, str):
            dt = str_to_dt(dt)
        self.dt = dt
        self.config = config
        self.lat: float = None
        self.lon: float = None
        self.timezone: str = None
        self.house_sys = house_sys
        self.houses: list[House] = []
        self.planets: list[Planet] = []
        self.extras: list[Extra] = []
        self.vertices: list[Vertex] = []
        self.signs: list[Sign] = []
        self.aspects: list[Aspect] = []
        self.quadrants: list[list[Aspectable]] = []
        self.set_lat_lon()
        self.set_houses_vertices()
        self.set_movable_bodies()
        self.set_aspectable()
        self.set_signs()
        self.set_normalized_degrees()
        self.set_aspects()
        self.set_rulers()
        self.set_quadrants()

    @property
    def julian_day(self) -> float:
        """
        Convert dt to UTC and return Julian day.

        Returns:
            float: The Julian day.
        """
        local_tz = ZoneInfo(self.timezone)
        local_dt = self.dt.replace(tzinfo=local_tz)
        utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
        return swe.date_conversion(
            utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60
        )[1]

    def set_lat_lon(self):
        """
        Set the geographical information of a city.
        """
        info = self.cities[
            self.cities["ascii_name"].str.lower() == self.city.lower()
        ].iloc[0]
        self.lat = float(info["lat"])
        self.lon = float(info["lon"])
        self.timezone = info["timezone"]

    def set_movable_bodies(self):
        """
        Set the positions of the planets and other celestial bodies.
        """
        self.planets = self.set_positions(PLANET_MEMBERS)
        self.extras = self.set_positions(EXTRA_MEMBERS)

    def set_houses_vertices(self) -> None:
        """
        Calculate the cusps of the houses and set the vertices.
        """
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

        self.vertices = [
            Vertex(degree=asc_deg, **VERTEX_MEMBERS[0]),
            Vertex(degree=(mc_deg + 180) % 360, **VERTEX_MEMBERS[1]),
            Vertex(degree=(asc_deg + 180) % 360, **VERTEX_MEMBERS[2]),
            Vertex(degree=mc_deg, **VERTEX_MEMBERS[3]),
        ]

        for v in self.vertices:
            setattr(self, v.name, v)

    def set_aspectable(self):
        """
        Set the aspectable celestial bodies based on the display configuration.
        """
        self.aspectables = [
            body
            for body in (self.planets + self.extras + self.vertices)
            if self.config.display[body.name]
        ]

    def set_signs(self):
        """
        Set the signs of the zodiac.
        """
        for i, sign_member in enumerate(SIGN_MEMBERS):
            sign = Sign(
                **sign_member,
                degree=i * 30,
            )
            self.signs.append(sign)

    def set_aspects(self):
        """
        Set the aspects between the aspectable celestial bodies.
        """
        body_pairs = pairs(self.aspectables)
        self.aspects = self.calculate_aspects(body_pairs)

    def set_normalized_degrees(self):
        """
        Normalize the positions of celestial bodies relative to the first house.
        """
        bodies = self.signs + self.planets + self.extras + self.vertices + self.houses
        for body in bodies:
            body.normalized_degree = self.normalize(body.degree)

    def set_rulers(self):
        """
        Set the rulers for each house.
        """
        for house in self.houses:
            ruler = getattr(self, house.sign.ruler)
            classic_ruler = getattr(self, house.sign.classic_ruler)
            house.ruler = ruler.name
            house.ruler_sign = f"{ruler.sign.symbol}"
            house.ruler_house = self.house_of(ruler)
            house.classic_ruler = classic_ruler.name
            house.classic_ruler_sign = (
                f"{classic_ruler.sign.symbol} {classic_ruler.sign.name}"
            )
            house.classic_ruler_house = self.house_of(classic_ruler)

    def set_quadrants(self):
        """
        Set the distribution of celestial bodies in quadrants.
        """
        bodies = [b for b in self.aspectables if b not in self.vertices]
        _, ic, dsc, mc = [v.normalized_degree for v in self.vertices]

        first = [b for b in bodies if b.normalized_degree < ic]
        second = [b for b in bodies if ic <= b.normalized_degree < dsc]
        third = [b for b in bodies if dsc <= b.normalized_degree < mc]
        fourth = [b for b in bodies if mc <= b.normalized_degree]
        self.quadrants = [first, second, third, fourth]

    def __str__(self):
        """
        String representation of the Data object.

        Returns:
            str: The string representation.
        """
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

    def set_positions(self, bodies: list[Body]) -> list[Aspectable]:
        """
        Set the positions of the planets and other celestial bodies.

        Args:
            bodies (list[Body]): The list of celestial bodies.

        Returns:
            list[Aspectable]: The list of aspectable bodies with positions set.
        """
        output = []
        for body in bodies:
            ((lon, _, _, speed, *_), _) = swe.calc_ut(self.julian_day, body.value)
            pos = Aspectable(
                **body,
                degree=lon,
                speed=speed,
            )
            setattr(self, body.name, pos)
            output.append(pos)
        return output

    def house_of(self, body: Body) -> int:
        """
        Get the house of a celestial body.

        Args:
            body (Body): The celestial body.

        Returns:
            int: The house number.
        """
        sorted_houses = sorted(self.houses, key=lambda x: x.degree, reverse=True)
        for house in sorted_houses:
            if body.degree >= house.degree:
                return house.value
        return sorted_houses[0].value

    def normalize(self, degree: float) -> float:
        """
        Normalize the degree relative to the first house.

        Args:
            degree (float): The degree to normalize.

        Returns:
            float: The normalized degree.
        """
        return (degree - self.asc.degree + 360) % 360

    def calculate_aspects(self, body_pairs: BodyPairs) -> list[Aspect]:
        """
        Calculate the aspects between pairs of celestial bodies.

        Args:
            body_pairs (BodyPairs): The pairs of celestial bodies.

        Returns:
            list[Aspect]: The list of aspects.
        """
        output = []
        for b1, b2 in body_pairs:
            sorted_bodies = sorted([b1, b2], key=lambda x: x.degree)
            org_angle = sorted_bodies[1].degree - sorted_bodies[0].degree
            # get the smaller angle
            angle = 360 - org_angle if org_angle > 180 else org_angle
            for aspect_member in ASPECT_MEMBERS:
                orb_val = self.config.orb[aspect_member.name]
                max_orb = aspect_member.value + orb_val
                min_orb = aspect_member.value - orb_val
                if min_orb <= angle <= max_orb:
                    applying = sorted_bodies[0].speed > sorted_bodies[1].speed
                    if angle < aspect_member.value:
                        applying = not applying
                    applying = not applying if org_angle > 180 else applying
                    output.append(
                        Aspect(
                            body1=b1,
                            body2=b2,
                            aspect_member=aspect_member,
                            applying=applying,
                            orb=abs(angle - aspect_member.value),
                        )
                    )
        return output

    def composite_aspects_pairs(self, data2: Self) -> BodyPairs:
        """
        Generate pairs of aspectable bodies for composite chart.

        Args:
            data2 (Data): The second data object.

        Returns:
            BodyPairs: The pairs of aspectable bodies.
        """
        return itertools.product(self.aspectables, data2.aspectables)
