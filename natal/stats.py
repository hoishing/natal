"""
This module provides statistical analysis for natal charts.

It contains the Stats class, which calculates and presents various astrological statistics
for a single natal chart or a comparison between two charts.
"""

from collections import defaultdict
from math import floor
from natal.classes import Aspect
from natal.data import Data
from tabulate import SEPARATING_LINE, tabulate
from typing import Iterable, Literal

DistKind = Literal["element", "quality", "polarity"]
Grid = list[Iterable[str | int]]


class Stats:
    """
    Statistics for a natal chart data.

    This class calculates and presents various astrological statistics for a single natal chart
    or a comparison between two charts.

    Attributes:
        data1 (Data): The primary natal chart data.
        data2 (Data | None): The secondary natal chart data for comparisons (optional).
        tb_option (dict): Default options for table formatting.
    """

    data1: Data
    data2: Data | None = None
    tb_option = dict(
        tablefmt="github",
        numalign="center",
        headers="firstrow",
    )

    def __init__(self, data1: Data, data2: Data = None) -> None:
        """
        Initialize the Stats object with one or two natal chart data sets.

        Args:
            data1 (Data): The primary natal chart data.
            data2 (Data, optional): The secondary natal chart data for comparisons.
        """
        self.data1 = data1
        self.data2 = data2
        if self.data2:
            self.composite_pairs = Data.composite_aspects_pairs(self.data2, self.data1)
            self.composite_aspects = Data.calculate_aspects(
                self.composite_pairs, self.data1.config.composite_orb
            )

    # data grids =================================================================

    def distribution_grid(self, kind: DistKind) -> Grid:
        """
        Generate a grid of distribution data for elements, qualities, or polarities.

        Args:
            kind (DistKind): The type of distribution to calculate ("element", "quality", or "polarity").

        Returns:
            Grid: A grid containing the distribution data.
        """
        bodies = defaultdict(lambda: [0, []])
        for body in self.data1.aspectables:
            key = body.sign[kind]
            bodies[key][0] += 1  # act as a counter
            bodies[key][1].append(f"{body.name} {body.sign.symbol}")
        grid = [(kind, "count", "bodies")]
        data = [(key, val[0], ", ".join(val[1])) for key, val in bodies.items()]
        grid.extend(data)
        return grid

    @property
    def celestial_body_grid(self) -> Grid:
        """
        Generate a grid of celestial body positions for the primary chart.

        Returns:
            Grid: A grid containing celestial body data (name, sign, and house).
        """
        grid = [("body", "sign", "house")]
        for body in self.data1.aspectables:
            grid.append((body.name, body.signed_dms, self.data1.house_of(body)))
        return grid

    @property
    def data2_celestial_body_grid(self) -> Grid:
        """
        Generate a grid of celestial body positions for the secondary chart.

        Returns:
            Grid: A grid containing celestial body data (name, sign, and house) for the secondary chart.
        """
        grid = [(self.data2.name, "sign", "house")]
        for body in self.data2.aspectables:
            grid.append((body.name, body.signed_dms, self.data1.house_of(body)))
        return grid

    @property
    def house_grid(self) -> Grid:
        """
        Generate a grid of house data for the primary chart.

        Returns:
            Grid: A grid containing house data (name, sign, ruler, ruler sign, and ruler house).
        """
        grid = [("house", "sign", "ruler", "ruler sign", "ruler house")]
        for house in self.data1.houses:
            grid.append(
                (
                    house.name,
                    house.signed_dms,
                    house.ruler,
                    house.ruler_sign,
                    house.ruler_house,
                )
            )
        return grid

    @property
    def quadrant_grid(self) -> Grid:
        """
        Generate a grid of celestial body distribution in quadrants.

        Returns:
            Grid: A grid containing quadrant distribution data.
        """
        quad_names = ["first", "second", "third", "fourth"]
        quadrants = defaultdict(lambda: [0, []])
        for i, quad in enumerate(self.data1.quadrants):
            if quad:
                for body in quad:
                    quadrants[i][0] += 1  # act as a counter
                    quadrants[i][1].append(f"{body.symbol} {body.name}")
            else:
                # no celestial body in this quadrant
                quadrants[i][0] = 0
        grid = [("quadrant", "count", "bodies")]
        data = [
            (quad_names[quad_no], val[0], ", ".join(val[1]))
            for quad_no, val in quadrants.items()
        ]
        return grid + data

    @property
    def hemisphere_grid(self) -> Grid:
        """
        Generate a grid of celestial body distribution in hemispheres.

        Returns:
            Grid: A grid containing hemisphere distribution data.
        """
        grid = [("hemisphere", "count", "bodies")]
        data = self.quadrant_grid[1:]
        eastern = ("eastern", data[0][1] + data[3][1], f"{data[0][2]}, {data[3][2]}")
        western = ("western", data[1][1] + data[2][1], f"{data[1][2]}, {data[2][2]}")
        northern = ("northern", data[2][1] + data[3][1], f"{data[2][2]}, {data[3][2]}")
        southern = ("southern", data[0][1] + data[1][1], f"{data[0][2]}, {data[1][2]}")
        return grid + [eastern, western, northern, southern]

    @property
    def data1_aspect_grid(self) -> Grid:
        """
        Generate a grid of aspects for the primary chart.

        Returns:
            Grid: A grid containing aspect data for the primary chart.
        """
        headers = ["body 1", "aspect", "body 2", "phase", "orb"]
        return self._aspect_grid(self.data1.aspects, headers)

    @property
    def composite_aspect_grid(self) -> Grid:
        """
        Generate a grid of composite aspects between two charts.

        Returns:
            Grid: A grid containing composite aspect data.
        """
        headers = [self.data2.name, "aspect", self.data1.name, "phase", "orb"]
        return self._aspect_grid(self.composite_aspects, headers)

    @property
    def aspect_cross_ref_grid(self) -> Grid:
        """
        Generate a grid for aspect cross-reference between charts or within a single chart.

        Returns:
            Grid: A grid containing aspect cross-reference data.
        """
        aspectable1 = self.data1.aspectables
        aspectable2 = self.data2.aspectables if self.data2 else self.data1.aspectables
        aspects = self.composite_aspects if self.data2 else self.data1.aspects
        body_symbols = [body.symbol for body in aspectable1]
        grid = [[""] + body_symbols + ["Total"]]  # Header row with Total column
        for body1 in aspectable1:
            row = [body1.symbol]
            aspect_count = 0
            for body2 in aspectable2:
                aspect = next(
                    (
                        asp
                        for asp in aspects
                        if (asp.body1 == body1 and asp.body2 == body2)
                        or (asp.body1 == body2 and asp.body2 == body1)
                    ),
                    None,
                )
                if aspect:
                    row.append(aspect.aspect_member.symbol)
                    aspect_count += 1
                else:
                    row.append(None)

            row.append(str(aspect_count))  # Add total count to the end of the row
            grid.append(row)
        return grid

    # tables =====================================================================

    def distribution_table(self, kind: DistKind) -> str:
        """
        Generate a formatted table of distribution data.

        Args:
            kind (DistKind): The type of distribution to display ("element", "quality", or "polarity").

        Returns:
            str: A formatted string containing the distribution table.
        """
        return self.draw_table(
            f"{kind.capitalize()} Distribution ({self.data1.name})",
            tabulate(self.distribution_grid(kind), **self.tb_option),
        )

    @property
    def celestial_body_table(self) -> str:
        """
        Generate a formatted table of celestial body positions for the primary chart.

        Returns:
            str: A formatted string containing the celestial body table.
        """
        return self.draw_table(
            f"Celestial Bodies ({self.data1.name})",
            tabulate(self.celestial_body_grid, **self.tb_option),
        )

    @property
    def house_table(self) -> str:
        """
        Generate a formatted table of house data for the primary chart.

        Returns:
            str: A formatted string containing the house table.
        """
        return self.draw_table(
            f"Houses ({self.data1.name})",
            tabulate(self.house_grid, **self.tb_option),
        )

    @property
    def quadrant_table(self) -> str:
        """
        Generate a formatted table of quadrant distribution data.

        Returns:
            str: A formatted string containing the quadrant distribution table.
        """
        return self.draw_table(
            f"Quadrants ({self.data1.name})",
            tabulate(self.quadrant_grid, **self.tb_option),
        )

    @property
    def hemisphere_table(self) -> str:
        """
        Generate a formatted table of hemisphere distribution data.

        Returns:
            str: A formatted string containing the hemisphere distribution table.
        """
        return self.draw_table(
            f"Hemispheres ({self.data1.name})",
            tabulate(self.hemisphere_grid, **self.tb_option),
        )

    @property
    def data1_aspect_table(self) -> str:
        """
        Generate a formatted table of aspects for the primary chart.

        Returns:
            str: A formatted string containing the aspect table for the primary chart.
        """
        return self.draw_table(
            f"Aspects ({self.data1.name})",
            tabulate(self.data1_aspect_grid, **self.tb_option),
        )

    @property
    def composite_aspect_table(self) -> str:
        """
        Generate a formatted table of composite aspects between two charts.

        Returns:
            str: A formatted string containing the composite aspect table.
        """
        return self.draw_table(
            f"Aspects of {self.data2.name} vs {self.data1.name}",
            tabulate(
                self.composite_aspect_grid,
                **self.tb_option,
                colalign=("left", "center", "left", "center"),
            ),
        )

    @property
    def data2_celestial_body_table(self) -> str:
        """
        Generate a formatted table of celestial body positions for the secondary chart.

        Returns:
            str: A formatted string containing the celestial body table for the secondary chart.
        """
        return self.draw_table(
            f"Celestial Bodies of {self.data2.name} in {self.data1.name}'s chart",
            tabulate(self.data2_celestial_body_grid, **self.tb_option),
        )

    @property
    def aspect_cross_ref_table(self) -> str:
        """
        Generate a formatted table for aspect cross-reference.

        Returns:
            str: A formatted string containing the aspect cross-reference table.
        """
        name = (
            f"{self.data2.name}(cols) vs {self.data1.name}(rows)"
            if self.data2
            else self.data1.name
        )
        return self.draw_table(
            f"Aspect Cross Reference of {name}",
            tabulate(
                self.aspect_cross_ref_grid,
                stralign="center",
                **self.tb_option | {"tablefmt": "simple_grid"},
            ),
        )

    # output =====================================================================

    @property
    def full_report(self) -> str:
        """
        Generate a full report containing all statistical tables.

        Returns:
            str: A formatted string containing the full statistical report.
        """
        output = "\n"
        for dist in ["element", "quality", "polarity"]:
            output += self.distribution_table(dist)
        output += self.celestial_body_table
        output += self.house_table
        output += self.quadrant_table
        output += self.hemisphere_table
        if self.data2:
            output += self.data2_celestial_body_table
            output += self.composite_aspect_table
        else:
            output += self.data1_aspect_table
        output += self.aspect_cross_ref_table
        return output

    # utils ======================================================================

    def draw_table(self, title: str, table: str) -> str:
        """
        Format a table with a title.

        Args:
            title (str): The title of the table.
            table (str): The table content as a string.

        Returns:
            str: A formatted string containing the titled table.
        """
        output = f"# {title}\n\n"
        output += table
        output += "\n\n\n"
        return output

    def _aspect_grid(self, aspects: list[Aspect], headers: list[str]) -> Grid:
        """
        Generate a grid of aspect data.

        Args:
            aspects (list[Aspect]): A list of Aspect objects.
            headers (list[str]): The headers for the aspect grid.

        Returns:
            Grid: A grid containing aspect data.
        """
        grid = [headers]
        for aspect in aspects:
            degree = floor(aspect.orb)
            minutes = round((aspect.orb - degree) * 60)
            grid.append(
                (
                    aspect.body1.name,
                    aspect.aspect_member.symbol,
                    aspect.body2.name,
                    "> <" if aspect.applying else "<->",
                    f"{degree}° {minutes:02d}'",
                )
            )
        return grid


# for quick testing
if __name__ == "__main__":
    from tests import person1, person2

    shing = Data(**person1)
    belle = Data(**person2)
    stats = Stats(data1=shing, data2=belle)
    print(stats.full_report)
