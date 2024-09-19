from math import radians, cos, sin
from natal.data import Data
from ptag import Tag, svg, path, circle, text, line
from natal.config import Config, load_config, Orb
from natal.const import SIGN_MEMBERS
from natal.utils import DotDict
from natal.classes import Aspect


class Chart(DotDict):
    """SVG representation of natal chart."""

    def __init__(
        self,
        data1: Data,
        width: int,
        height: int | None = None,
        data2: Data | None = None,
        config: Config = load_config(),
    ):
        self.data1 = data1
        self.data2 = data2
        self.width = width
        self.height = height
        if self.height is None:
            self.height = self.width
        self.cx = self.width / 2
        self.cy = self.height / 2

        self.config = config
        margin = min(self.width, self.height) * config.chart.margin_factor
        self.max_radius = min(self.width - margin, self.height - margin) // 2
        self.ring_thickness = self.max_radius * config.chart.ring_thickness_fraction
        self.font_size = self.ring_thickness * self.config.chart.font_size_fraction

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
        stroke_opacity: float = 1,
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
            "",
            d=path_data,
            fill=fill,
            stroke=stroke_color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
        )

    def background(self, radius: float, **kwargs) -> Tag:
        return circle(cx=self.cx, cy=self.cy, r=radius, **kwargs)

    def sign_wheel(self) -> list[Tag]:

        radius = self.max_radius

        wheel = [self.background(radius=radius, fill=self.config.theme.background)]
        for i in range(12):
            start_deg = (i * 30 - self.data1.houses[0].degree) % 360
            end_deg = start_deg + 30
            wheel.append(
                self.sector(
                    radius=radius,
                    start_deg=start_deg,
                    end_deg=end_deg,
                    fill=self.fill_color(i, bg=True),
                    stroke_color=self.config.theme.foreground,
                    stroke_width=self.config.chart.stroke_width,
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
                    font_family=self.config.chart.font,
                    font_size=symbol_width,
                    text_anchor="middle",
                    dominant_baseline="central",
                )
            )

        return wheel

    def house_wheel(self) -> list[Tag]:
        radius = self.max_radius - self.ring_thickness

        wheel = [self.background(radius, fill=self.config.theme.background)]
        for i in range(12):
            next_i = (i + 1) % 12
            start_deg = self.data1.houses[i].normalized_degree
            end_deg = self.data1.houses[next_i].normalized_degree

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
                    stroke_width=self.config.chart.stroke_width,
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
            wheel.append(
                text(
                    str(i + 1),  # House numbers start from 1
                    x=number_x,
                    y=number_y,
                    fill=self.fill_color(i),
                    font_family=self.config.chart.font,
                    font_size=number_width,
                    text_anchor="middle",
                    dominant_baseline="central",
                )
            )

        return wheel

    def vertex_line(self) -> list[Tag]:
        vertex_radius = self.max_radius + self.ring_thickness
        house_radius = self.max_radius - 2 * self.ring_thickness
        body_radius = self.max_radius - 3 * self.ring_thickness

        lines = [
            self.background(
                house_radius,
                fill=self.config.theme.background,
                stroke=self.config.theme.foreground,
                stroke_width=self.config.chart.stroke_width,
            ),
            self.background(
                body_radius,
                fill="#88888800",
                stroke=self.config.theme.dim,
                stroke_width=self.config.chart.stroke_width,
            ),
        ]
        for house in self.data1.houses:
            radius = house_radius
            stroke_width = self.config.chart.stroke_width
            stroke_color = self.config.theme.dim

            if house.value in [1, 4, 7, 10]:
                radius = vertex_radius
                stroke_color = self.config.theme.foreground

            angle = radians(house.normalized_degree)
            end_x = self.cx - radius * cos(angle)
            end_y = self.cy + radius * sin(angle)

            lines.append(
                line(
                    x1=self.cx,
                    y1=self.cy,
                    x2=end_x,
                    y2=end_y,
                    stroke=stroke_color,
                    stroke_width=stroke_width,
                    stroke_opacity=self.config.chart.stroke_opacity,
                )
            )

        return lines

    def outer_body_wheel(self) -> list[Tag]:
        radius = self.max_radius - 3 * self.ring_thickness
        data = self.data2 or self.data1
        return self.body_wheel(radius, data, self.config.chart.outer_min_degree)

    def inner_body_wheel(self) -> list[Tag] | None:
        if self.data2 is None:
            return
        radius = self.max_radius - 4 * self.ring_thickness
        data = self.data1
        return self.body_wheel(radius, data, self.config.chart.inner_min_degree)

    def outer_aspect(self) -> list[Tag]:
        if self.data2 is not None:
            return []
        radius = self.max_radius - 3 * self.ring_thickness
        orb = self.config.orb
        aspects = self.data1.aspects
        return self.aspect_lines(radius, orb, aspects)

    def inner_aspect(self) -> list[Tag]:
        if self.data2 is None:
            return []
        radius = self.max_radius - 4 * self.ring_thickness
        orb = self.config.composite_orb
        aspects = Data.calculate_aspects(
            Data.composite_aspects_pairs(self.data1, self.data2),
            orb=orb,
        )
        return self.aspect_lines(radius, orb, aspects)

    # utils ======================================================

    def adjusted_degrees(
        self, sorted_degrees: list[float], min_degree: float
    ) -> list[float]:
        """adjust spacing between celestial bodies to avoid overlap"""

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

    def fill_color(self, sign_no: int, bg: bool = False) -> str:
        fill_hex = getattr(self.config.theme, SIGN_MEMBERS[sign_no].color)
        if not bg:
            return fill_hex
        trans_fill_hex = f"{fill_hex}{int(self.config.theme.transparency * 255):02x}"
        return trans_fill_hex

    def body_wheel(self, radius: float, data: Data, min_degree: float):
        """common steps for drawing inner and outer body wheel"""

        sorted_aspectables = sorted(data.aspectables, key=lambda x: x.degree)
        # normalize relative to first house of data1
        sorted_degrees = [
            self.data1.normalize(body.degree) for body in sorted_aspectables
        ]

        # Calculate adjusted positions
        adjusted_degrees = self.adjusted_degrees(sorted_degrees, min_degree)

        output = []
        for body, adjusted_degree in zip(sorted_aspectables, adjusted_degrees):
            font_size = self.font_size
            text_opt = {}

            # special handling for asc and mc
            if body.name in ["asc", "mc"]:
                text_opt = {
                    "lengthAdjust": "spacingAndGlyphs",
                    "textLength": self.font_size * 0.7,
                }
                font_size *= 0.85

            symbol_radius = radius + (self.ring_thickness / 2)
            degree_radius = radius

            # Use original angle for line start position
            original_angle = radians(self.data1.normalize(body.degree))
            degree_x = self.cx - degree_radius * cos(original_angle)
            degree_y = self.cy + degree_radius * sin(original_angle)

            # Use adjusted angle for symbol position
            adjusted_angle = radians(adjusted_degree)
            symbol_x = self.cx - symbol_radius * cos(adjusted_angle)
            symbol_y = self.cy + symbol_radius * sin(adjusted_angle)

            # Add line connecting to the inner circle
            inner_radius = self.max_radius - 4 * self.ring_thickness
            inner_x = self.cx - inner_radius * cos(original_angle)
            inner_y = self.cy + inner_radius * sin(original_angle)

            output.extend(
                [
                    line(
                        x1=degree_x,
                        y1=degree_y,
                        x2=symbol_x,
                        y2=symbol_y,
                        stroke=self.config.theme[body.color],
                        stroke_width=self.config.chart.stroke_width / 2,
                    ),
                    circle(
                        cx=symbol_x,
                        cy=symbol_y,
                        r=font_size / 2,
                        fill=self.config.theme.background,
                    ),
                    line(
                        x1=degree_x,
                        y1=degree_y,
                        x2=inner_x,
                        y2=inner_y,
                        stroke=self.config.theme.dim,
                        stroke_width=self.config.chart.stroke_width / 2,
                        stroke_dasharray=self.ring_thickness / 11,
                    ),
                    text(
                        body.symbol,
                        x=symbol_x,
                        y=symbol_y,
                        fill=self.config.theme[body.color],
                        font_family=self.config.chart.font,
                        font_size=font_size,
                        text_anchor="middle",
                        dominant_baseline="central",
                        **text_opt,
                    ),
                ]
            )
        return output

    def aspect_lines(self, radius: float, orb: Orb, aspects: list[Aspect]) -> list[Tag]:
        """draw aspect lines between aspectables"""

        output = [
            self.background(
                radius,
                fill=self.config.theme.background,
                stroke=self.config.theme.dim,
                stroke_width=self.config.chart.stroke_width,
            )
        ]
        for aspect in aspects:
            start_angle = radians(self.data1.normalize(aspect.body1.degree))
            end_angle = radians(self.data1.normalize(aspect.body2.degree))
            orb_fraction = 1 - aspect.orb / orb[aspect.aspect_member.name]
            opacity_factor = (
                1 if aspect.aspect_member.name == "conjunction" else orb_fraction
            )
            output.append(
                line(
                    x1=self.cx - radius * cos(start_angle),
                    y1=self.cy + radius * sin(start_angle),
                    x2=self.cx - radius * cos(end_angle),
                    y2=self.cy + radius * sin(end_angle),
                    stroke=self.config.theme[aspect.aspect_member.color],
                    stroke_width=self.config.chart.stroke_width / 2,
                    stroke_opacity=self.config.chart.stroke_opacity * opacity_factor,
                )
            )
        return output
