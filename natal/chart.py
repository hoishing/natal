from math import radians, cos, sin
from pydantic.dataclasses import dataclass
from pydantic import Field
from natal.natal_data import NatalData
from ptag import Tag, svg, path, circle, text, g, line
from natal.enums import Points, Element, Sign
from natal.config import Config, load_config


@dataclass
class Chart:
    """SVG representation of natal chart."""

    natal_data: NatalData
    width: int
    height: int | None = None
    config: Config = Field(default_factory=load_config)

    def __post_init__(self):
        if self.height is None:
            self.height = self.width

    @property
    def svg_root(self) -> Tag:
        """Generate an SVG element with sensible defaults"""

        return svg(
            "",
            height=self.height,
            width=self.width,
            # viewbox=None,
            version="1.1",
            xmlns="http://www.w3.org/2000/svg",
        )

    def sector(
        self,
        radius: int,
        start_deg: float,
        end_deg: float,
        fill: str = "white",
        stroke: str = "black",
        stroke_width: float = 1,
    ) -> Tag:
        """
        Creates a sector shape in SVG format.

        Args:
            radius (int): The radius of the sector.
            start_deg (float): The starting angle of the sector in degrees.
            end_deg (float): The ending angle of the sector in degrees.
            fill (str, optional): The fill color of the sector. Defaults to "white".
            stroke (str, optional): The stroke color of the sector. Defaults to "black".
            stroke_width (float, optional): The stroke width of the sector. Defaults to 1.

        Returns:
            Tag: The SVG tag representing the sector shape.

        Example:
            >>> sector(100, 100, 50, 0, 90)
            <path d="M100 100 L50.0 100.0 A50 50 0 0 0 100.0 150.0 Z" fill="white" stroke="black" stroke-width="1"></path>
        """
        center_x: float = self.width / 2
        center_y: float = self.height / 2
        start_rad = radians(start_deg)
        end_rad = radians(end_deg)
        start_x = center_x - radius * cos(start_rad)
        start_y = center_y + radius * sin(start_rad)
        end_x = center_x - radius * cos(end_rad)
        end_y = center_y + radius * sin(end_rad)

        start_x, start_y, end_x, end_y = [
            round(val, 2) for val in (start_x, start_y, end_x, end_y)
        ]

        path_data = " ".join(
            (
                "M{} {}".format(center_x, center_y),
                "L{} {}".format(start_x, start_y),
                "A{} {} 0 0 0 {} {}".format(radius, radius, end_x, end_y),
                "Z",
            )
        )
        return path(
            "", d=path_data, fill=fill, stroke=stroke, stroke_width=stroke_width
        )

    def wheel(
        self,
        radius: int | None = None,
        stroke_width: int = 1,
    ) -> Tag:
        """
        Creates a wheel shape in SVG format.

        Returns:
            Tag: The SVG tag representing the wheel shape.
        """

        max_radius = min(self.width, self.height) // 2

        if radius is None:
            radius = max_radius

        if radius > max_radius:
            raise ValueError(f"{radius=} > half of the chart: {max_radius}")

        # offset from asc in NatalData.entities
        offset = self.natal_data.get_entity(Points.asc).degree

        for i in range(12):
            start_deg = i * 30 + offset
            end_deg = start_deg + 30
            fill_hex = getattr(self.config.theme, Sign(i + 1).color_name)
            self.sector(
                radius=radius,
                start_deg=start_deg,
                end_deg=end_deg,
                fill=fill_hex,
                stroke=self.config.theme.foreground,
                stroke_width=stroke_width,
            )
