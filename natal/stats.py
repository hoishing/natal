from math import floor
from typing import Literal
from natal.data import Data
from collections import defaultdict
from tabulate import tabulate


DistKind = Literal["element", "quality", "polarity"]
Grid = list[list[str | int]]


class Stats:
    """Statistics for a natal chart data"""

    data: Data
    element_counts: Grid = None
    quality_counts: Grid = None
    polarity_counts: Grid = None

    def __init__(self, data: Data) -> None:
        self.data = data

    def distribution_table(self, kind: DistKind) -> str:
        """distribution of celestial bodies"""
        bodies = defaultdict(lambda: [0, []])
        for body in self.data.aspectables:
            key = body.sign[kind]
            bodies[key][0] += 1  # act as a counter
            bodies[key][1].append(f"{body.name} {body.sign.symbol}")
        grid = [(kind, "count", "bodies")]
        data = [(key, val[0], ", ".join(val[1])) for key, val in bodies.items()]
        grid.extend(data)
        setattr(self, f"{kind}_counts", grid)
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

    def quadrant_table(self) -> str:
        pass

    @property
    def aspectable_body_table(self) -> str:
        """distribution of movable bodies"""
        grid = [("body", "sign", "house")]
        for body in self.data.aspectables:
            grid.append((body.name, body.signed_dms, self.data.house_of(body.name)))
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

    @property
    def aspect_table(self) -> str:
        grid = [("body 1", "aspect", "body 2", "phase", "orb")]
        for aspect in self.data.aspects:
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
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

    @property
    def aspect_grid(self) -> str:
        body_symbols = [body.symbol for body in self.data.aspectables]
        grid = [[""] + body_symbols + ["Total"]]  # Header row with Total column

        for i, body1 in enumerate(self.data.aspectables):
            row = [body1.symbol]
            aspect_count = 0
            for j, body2 in enumerate(self.data.aspectables):
                aspect = next(
                    (
                        asp
                        for asp in self.data.aspects
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

        return tabulate(
            grid,
            headers="firstrow",
            tablefmt="simple_grid",
            stralign="center",
            numalign="center",
        )

    @property
    def house_table(self) -> str:
        grid = [("house", "sign", "ruler", "ruler sign", "ruler house")]
        for house in self.data.houses:
            grid.append(
                (
                    house.name,
                    house.signed_dms,
                    house.ruler,
                    house.ruler_sign,
                    house.ruler_house,
                )
            )
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

    @property
    def quadrant_table(self) -> str:
        """distribution of celestial bodies in quadrants"""
        quad_names = ["first", "second", "third", "fourth"]
        quadrants = defaultdict(lambda: [0, []])
        for i, quad in enumerate(self.data.quadrants):
            for body in quad:
                quadrants[i][0] += 1  # act as a counter
                quadrants[i][1].append(f"{body.symbol} {body.name}")
        grid = [("quadrant", "count", "bodies")]
        data = [
            (quad_names[quad_no], val[0], ", ".join(val[1]))
            for quad_no, val in quadrants.items()
        ]

        left = ("left", data[0][1] + data[3][1], f"{data[0][2]}, {data[3][2]}")
        right = ("right", data[1][1] + data[2][1], f"{data[1][2]}, {data[2][2]}")
        upper = ("upper", data[2][1] + data[3][1], f"{data[2][2]}, {data[3][2]}")
        lower = ("lower", data[0][1] + data[1][1], f"{data[0][2]}, {data[1][2]}")
        separator = [(" --- ", " --- ", " --- ")]
        grid.extend(data + separator + [left, right, upper, lower])
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

    @property
    def full_report(self) -> str:
        output = "\n"
        for dist in ["element", "quality", "polarity"]:
            output += f"# {dist.capitalize()} Distribution\n\n"
            output += self.distribution_table(dist)
            output += "\n\n\n"
        output += "# Celestial Bodies\n\n"
        output += self.aspectable_body_table
        output += "\n\n\n"
        output += "# Quadrants\n\n"
        output += self.quadrant_table
        output += "\n\n\n"
        output += "# Houses\n\n"
        output += self.house_table
        output += "\n\n\n"
        output += "# Aspects\n\n"
        output += self.aspect_table
        output += "\n\n\n"
        output += "# Aspect Grid\n\n"
        output += self.aspect_grid
        output += "\n\n"
        return output


# for quick testing
if __name__ == "__main__":
    from natal.config import Config

    options = dict(
        display=dict(
            chiron=True,
        )
    )

    data = Data(
        name="shing", city="hong kong", dt="1976-04-20 18:58", config=Config(**options)
    )
    stats = Stats(data=data)
    print(stats.full_report)
