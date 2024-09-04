from typing import Literal
from natal.data import Data, MovableBody
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
        for body in self.data.aspectable:
            key = body.sign[kind]
            bodies[key][0] += 1  # act as a counter
            bodies[key][1].append(f"{body.name} {body.sign.symbol}")
        grid = [(kind, "count", "bodies")]
        data = [(key, val[0], ", ".join(val[1])) for key, val in bodies.items()]
        grid.extend(data)
        setattr(self, f"{kind}_counts", grid)
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

    def quadrant_table(self) -> str: ...

    @property
    def aspectable_body_table(self) -> str:
        """distribution of movable bodies"""
        grid = [("body", "sign", "house")]
        for body in self.data.aspectable:
            grid.append((body.name, body.signed_dms, self.data.body_houses[body.name]))
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

    @property
    def aspect_table(self) -> str:
        grid = [("body 1", "aspect", "body 2", "approaching", "orb")]
        for aspect in self.data.aspects:
            grid.append(
                (
                    aspect.body1.name,
                    aspect.aspect_type.symbol,
                    aspect.body2.name,
                    aspect.approaching,
                    aspect.orb,
                )
            )
        return tabulate(grid, headers="firstrow", tablefmt="orgtbl")

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
    def full_report(self) -> str:
        output = "\n"
        for dist in ["element", "quality", "polarity"]:
            output += f"# {dist.capitalize()} Distribution\n\n"
            output += self.distribution_table(dist)
            output += "\n\n\n"
        output += "# Celestial Bodies\n\n"
        output += self.aspectable_body_table
        output += "\n\n\n"
        output += "# Houses\n\n"
        output += self.house_table
        output += "\n\n\n"
        output += "# Aspects\n\n"
        output += self.aspect_table
        output += "\n\n"
        return output
