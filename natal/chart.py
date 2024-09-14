from math import radians, cos, sin, pi
from natal.classes import Aspectable
from natal.data import Data
from ptag import Tag, svg, path, circle, text, g, line, rect
from natal.config import Config, load_config
from natal.const import SIGN_MEMBERS
from natal.utils import DotDict


class Chart(DotDict):
    """SVG representation of natal chart."""

    config: Config = load_config()
    stroke_width: int = 1
    margin: int = 5
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
        self.aspectables: list[Tag] = []

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
        """Creates a sector shape in SVG format."""

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
                    fill=self.fill_color(i, bg=True),
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
            wheel.append(
                text(
                    SIGN_MEMBERS[i].symbol,
                    x=symbol_x,
                    y=symbol_y,
                    fill=self.fill_color(i),
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
    ) -> list[Tag]:
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
                    fill=self.fill_color(i, bg=True),
                    stroke_color=self.config.theme.foreground,
                    stroke_width=self.stroke_width,
                )
            )

            # Add house number
            number_width = self.font_size * 0.8
            number_radius = radius - (self.ring_thickness / 2)
            number_angle = radians(
                start_deg + ((end_deg - start_deg) % 360) / 2
            )  # Center of the house
            number_x = self.cx - number_radius * cos(number_angle)
            number_y = self.cy + number_radius * sin(number_angle)
            self.aspectables.append(
                text(
                    str(i + 1),  # House numbers start from 1
                    x=number_x,
                    y=number_y,
                    fill=self.fill_color(i),
                    font_family=self.font,
                    font_size=number_width,
                    text_anchor="middle",
                    dominant_baseline="central",
                )
            )

        return wheel

    def natal_body_wheel(
        self,
        radius: int | None = None,
    ) -> list[Tag]:
        if radius is None:
            radius = self.max_radius - (2 * self.ring_thickness)
        sorted_aspectables = sorted(self.data.aspectable, key=lambda x: x.degree)
        sorted_degrees = [body.normalized_degree for body in sorted_aspectables]

        output = [self.background(radius)]

        # Calculate minimum angle in radians
        min_degree: float = 7  # Adjust this value as needed

        # Calculate adjusted positions
        adjusted_degrees = self.adjusted_degrees(sorted_degrees, min_degree)

        for body, adjusted_degree in zip(sorted_aspectables, adjusted_degrees):
            font_size = (
                self.font_size
                if body.name not in ["asc", "mc"]
                else self.font_size * 0.7
            )
            symbol_radius = radius - (self.ring_thickness / 2)
            degree_radius = radius

            # Use original angle for line start position
            original_angle = radians(body.normalized_degree)
            degree_x = self.cx - degree_radius * cos(original_angle)
            degree_y = self.cy + degree_radius * sin(original_angle)

            # Use adjusted angle for symbol position
            adjusted_angle = radians(adjusted_degree)
            symbol_x = self.cx - symbol_radius * cos(adjusted_angle)
            symbol_y = self.cy + symbol_radius * sin(adjusted_angle)

            # Add line from degree position to symbol position
            output.append(
                line(
                    x1=degree_x,
                    y1=degree_y,
                    x2=symbol_x,
                    y2=symbol_y,
                    stroke=getattr(self.config.theme, body.color),
                    stroke_width=self.stroke_width / 2,
                )
            )
            self.aspectables.append(
                g()
                .add(
                    rect(
                        x=symbol_x - font_size / 2,
                        y=symbol_y - font_size / 2,
                        width=font_size,
                        height=font_size,
                        fill=self.config.theme.background,
                        rx=font_size / 4,  # Rounded corners
                    )
                )
                .add(
                    text(
                        body.symbol,
                        x=symbol_x,
                        y=symbol_y,
                        fill=getattr(self.config.theme, body.color),
                        font_family=self.font,
                        font_size=font_size,
                        text_anchor="middle",
                        dominant_baseline="central",
                    )
                )
            )

        return output + self.aspectables

    def vertex_line(self, radius: int | None = None) -> list[Tag]:
        if radius is None:
            radius = self.max_radius + self.ring_thickness

        lines = []
        for vertex in self.data.vertices:
            original_angle = radians(self.normalize(vertex.degree))
            end_x = self.cx - radius * cos(original_angle)
            end_y = self.cy + radius * sin(original_angle)

            lines.append(
                line(
                    x1=self.cx,
                    y1=self.cy,
                    x2=end_x,
                    y2=end_y,
                    stroke=self.config.theme.foreground,
                    stroke_width=self.stroke_width,
                )
            )

        return lines

    # utils ======================================================

    def adjusted_degrees(
        self, sorted_degrees: list[float], min_degree: float
    ) -> list[float]:
        forward_adjusted_degrees: list[float] = []
        backward_adjusted_degrees: list[float] = []
        last_degree: float | None = None

        # Forward adjustment
        for degree in sorted_degrees:
            current_degree = degree
            if last_degree is not None:
                if (current_degree - last_degree) % 360 < min_degree:
                    current_degree = (last_degree + min_degree) % 360
            forward_adjusted_degrees.append(current_degree)
            last_degree = current_degree

        # Backward adjustment
        last_degree = sorted_degrees[-1]  # Start with the last degree
        backward_adjusted_degrees = [last_degree]  # Add the last degree as anchor
        for degree in reversed(sorted_degrees[:-1]):  # Skip the last degree
            current_degree = degree
            if (last_degree - current_degree) % 360 < min_degree:
                current_degree = (last_degree - min_degree) % 360
            backward_adjusted_degrees.append(current_degree)
            last_degree = current_degree

        backward_adjusted_degrees.reverse()

        # Choose the adjustment that moves the points the least
        final_adjusted_degrees = []
        for fwd, bwd in zip(forward_adjusted_degrees, backward_adjusted_degrees):
            avg = ((fwd + bwd) / 2) % 360
            final_adjusted_degrees.append(avg)

        return final_adjusted_degrees

    def normalize(self, degree: float) -> float:
        """Normalize an angle to start from 180(Asc)"""
        return (degree - self.data.houses[0].degree) % 360

    def fill_color(self, sign_no: int, bg: bool = False) -> str:
        fill_hex = getattr(self.config.theme, SIGN_MEMBERS[sign_no].color)
        if not bg:
            return fill_hex
        trans_fill_hex = f"{fill_hex}{int(self.config.theme.transparency * 255):02x}"
        return trans_fill_hex
