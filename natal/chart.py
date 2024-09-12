from math import radians, cos, sin
from natal.data import Data
from ptag import Tag, svg, path, circle, text, g, line
from natal.config import Config, load_config
from natal.const import SIGN_MEMBERS
from natal.utils import DotDict


class Chart(DotDict):
    """SVG representation of natal chart."""

    data: Data
    width: int
    height: int | None = None
    config: Config = load_config()
    stroke_width: int = 1
    margin: int = 5
    ring_thickness: int = 0
    font: str = "Arial Unicode MS, sans-serif"
    font_size_fraction: float = 0.55

    def __init__(self, data: Data, width: int, height: int | None = None):
        self.data = data
        self.width = width
        self.height = height
        if self.height is None:
            self.height = self.width
        self.cx = self.width / 2
        self.cy = self.height / 2
        self.max_radius = min(self.width - self.margin, self.height - self.margin) // 2
        self.ring_thickness = self.max_radius * 0.15
        self.font_size = self.ring_thickness * self.font_size_fraction

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
        stroke_color: str = "black",
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
        start_rad = radians(start_deg)
        end_rad = radians(end_deg)
        start_x = self.cx - radius * cos(start_rad)
        start_y = self.cy + radius * sin(start_rad)
        end_x = self.cx - radius * cos(end_rad)
        end_y = self.cy + radius * sin(end_rad)

        start_x, start_y, end_x, end_y = [
            round(val, 2) for val in (start_x, start_y, end_x, end_y)
        ]

        path_data = " ".join(
            (
                "M{} {}".format(self.cx, self.cy),
                "L{} {}".format(start_x, start_y),
                "A{} {} 0 0 0 {} {}".format(radius, radius, end_x, end_y),
                "Z",
            )
        )
        return path(
            "", d=path_data, fill=fill, stroke=stroke_color, stroke_width=stroke_width
        )

    def background(self, radius: int | None = None) -> Tag:
        if radius is None:
            radius = self.max_radius

        return circle(
            cx=self.cx,
            cy=self.cy,
            r=radius,
            fill=self.config.theme.background,
            stroke=self.config.theme.foreground,
            stroke_width=self.stroke_width,
        )

    def sign_wheel(
        self,
        radius: int | None = None,
        stroke_width: int = 1,
    ) -> list[Tag]:
        """
        Creates a wheel shape in SVG format.

        Returns:
            Tag: The SVG tag representing the wheel shape.
        """

        if radius is None:
            radius = self.max_radius

        wheel = [self.background(radius)]
        for i in range(12):
            start_deg = self.normalize(i * 30)
            end_deg = start_deg + 30
            wheel.append(
                self.sector(
                    radius=radius,
                    start_deg=start_deg,
                    end_deg=end_deg,
                    fill=self.fill_color(i),
                    stroke_color=self.config.theme.foreground,
                    stroke_width=stroke_width,
                )
            )

            # Add sign symbol
            symbol_width = self.font_size
            symbol_radius = radius - (self.ring_thickness / 2)
            symbol_angle = radians(start_deg + 15)  # Center of the sector
            symbol_x = self.cx - symbol_radius * cos(symbol_angle)
            symbol_y = self.cy + symbol_radius * sin(symbol_angle)
            symbol_color = getattr(self.config.theme, SIGN_MEMBERS[i].color)
            wheel.append(
                text(
                    SIGN_MEMBERS[i].symbol,
                    x=symbol_x,
                    y=symbol_y,
                    fill=symbol_color,
                    font_family=self.font,
                    font_size=symbol_width,
                    text_anchor="middle",
                    dominant_baseline="central",
                )
            )

        return wheel

    def house_wheel(
        self,
        radius: int | None = None,
    ) -> Tag:
        if radius is None:
            radius = self.max_radius - self.ring_thickness

        wheel = [self.background(radius)]
        for i in range(12):
            next_i = (i + 1) % 12
            start_deg = self.normalize(self.data.houses[i].degree)
            end_deg = self.normalize(self.data.houses[next_i].degree)
            
            # Handle the case where end_deg is less than start_deg (crosses 0°)
            if end_deg < start_deg:
                end_deg += 360

            wheel.append(
                self.sector(
                    radius=radius,
                    start_deg=start_deg,
                    end_deg=end_deg,
                    fill=self.fill_color(i),
                    stroke_color=self.config.theme.foreground,
                    stroke_width=self.stroke_width,
                )
            )

            # Add house number
            number_width = self.font_size * 0.8
            number_radius = radius - (self.ring_thickness / 2)
            number_angle = radians(start_deg + ((end_deg - start_deg) % 360) / 2)  # Center of the house
            number_x = self.cx - number_radius * cos(number_angle)
            number_y = self.cy + number_radius * sin(number_angle)
            number_color = getattr(self.config.theme, SIGN_MEMBERS[i].color)
            wheel.append(
                text(
                    str(i + 1),  # House numbers start from 1
                    x=number_x,
                    y=number_y,
                    fill=number_color,
                    font_family=self.font,
                    font_size=number_width,
                    text_anchor="middle",
                    dominant_baseline="central",
                )
            )

        return wheel

    def body_wheel(
        self,
        radius: int | None = None,
    ) -> Tag:
        if radius is None:
            radius = self.max_radius - (2 * self.ring_thickness)

        wheel = [self.background(radius)]
        return wheel

    # utils ======================================================

    def normalize(self, degree: float) -> float:
        """Normalize an angle to start from 180(Asc)"""
        return (degree - self.data.houses[0].degree) % 360

    def fill_color(self, sign_no: int) -> str:
        fill_hex = getattr(self.config.theme, SIGN_MEMBERS[sign_no].color)
        trans_fill_hex = f"{fill_hex}{int(self.config.theme.transparency * 255):02x}"
        return trans_fill_hex
