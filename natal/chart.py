from math import radians, cos, sin
from dataclasses import dataclass
from natal.natal_data import NatalData
from ptag import Tag, svg, path, circle, text, g, line


@dataclass
class Chart:
    """SVG representation of natal chart."""

    natal_data: NatalData
    width: int = 1000
    height: int = 1000

    def svg_root(
        height: int,
        width: int,
        viewbox: str | None = None,
        version: str = "1.1",
        xmlns: str = "http://www.w3.org/2000/svg",
    ) -> Tag:
        """
        Generate an SVG element with sensible defaults.

        Parameters:
            height (int): The height of the SVG element.
            width (int): The width of the SVG element.
            viewbox (str, optional): The viewbox of the SVG element. Defaults to None.
            version (str, optional): The version of SVG. Defaults to "1.1".
            xmlns (str, optional): The XML namespace of SVG. Defaults to "http://www.w3.org/2000/svg".

        Returns:
            svg_tag: The generated SVG element.

        Example:
            >>> svg("", 100, 100)
            '<svg height="100" width="100" version="1.1" xmlns="http://www.w3.org/2000/svg"></svg>'

        """
        return svg(
            "",
            height=height,
            width=width,
            viewbox=viewbox,
            version=version,
            xmlns=xmlns,
        )

    def sector(
        center_x: int,
        center_y: int,
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
            center_x (int): The x-coordinate of the center of the sector.
            center_y (int): The y-coordinate of the center of the sector.
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

    def __str__(self) -> str:
        pass
