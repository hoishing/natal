from collections import defaultdict
from math import floor
from natal.classes import Aspect
from natal.data import Data
from tabulate import SEPARATING_LINE, tabulate
from typing import Literal

DistKind = Literal["element", "quality", "polarity"]
Grid = list[list[str | int]]


class Stats:
    """Statistics for a natal chart data"""

    data1: Data
    data2: Data | None = None
    element_counts: Grid = None
    quality_counts: Grid = None
    polarity_counts: Grid = None
    tb_option = dict(
        tablefmt="github",
        numalign="center",
        headers="firstrow",
    )

    def __init__(self, data1: Data, data2: Data = None) -> None:
        self.data1 = data1
        self.data2 = data2
        if self.data2:
            self.composite_pairs = Data.composite_aspects_pairs(self.data2, self.data1)
            self.composite_aspects = Data.calculate_aspects(
                self.composite_pairs, self.data1.config.composite_orb
            )

    def distribution_table(self, kind: DistKind) -> str:
        """distribution of celestial bodies"""
        bodies = defaultdict(lambda: [0, []])
        for body in self.data1.aspectables:
            key = body.sign[kind]
            bodies[key][0] += 1  # act as a counter
            bodies[key][1].append(f"{body.name} {body.sign.symbol}")
        grid = [(kind, "count", "bodies")]
        data = [(key, val[0], ", ".join(val[1])) for key, val in bodies.items()]
        grid.extend(data)
        setattr(self, f"{kind}_counts", grid)
        return tabulate(grid, **self.tb_option)

    def quadrant_table(self) -> str:
        pass

    @property
    def aspectable_body_table(self) -> str:
        """distribution of movable bodies"""
        grid = [("body", "sign", "house")]
        for body in self.data1.aspectables:
            grid.append((body.name, body.signed_dms, self.data1.house_of(body)))
        return tabulate(grid, **self.tb_option)

    @property
    def data2_aspectable_body_table(self) -> str:
        """distribution of data2 movable bodies"""
        grid = [("body", "sign", "house")]
        for body in self.data2.aspectables:
            grid.append((body.name, body.signed_dms, self.data1.house_of(body)))
        return tabulate(grid, **self.tb_option)

    @property
    def aspect_table(self) -> str:
        headers = ["body 1", "aspect", "body 2", "phase", "orb"]
        return self.draw_aspect_table(self.data1.aspects, headers)

    @property
    def composite_aspect_table(self) -> str:
        headers = [self.data2.name, "aspect", self.data1.name, "phase", "orb"]
        return self.draw_aspect_table(self.composite_aspects, headers)

    @property
    def aspect_grid(self) -> str:
        return self.draw_aspect_grid(self.data1, self.data1, self.data1.aspects)

    @property
    def composite_aspect_grid(self) -> str:
        return self.draw_aspect_grid(self.data1, self.data2, self.composite_aspects)

    @property
    def house_table(self) -> str:
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
        return tabulate(grid, **self.tb_option)

    @property
    def quadrant_table(self) -> str:
        """distribution of celestial bodies in quadrants"""
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

        left = ("left", data[0][1] + data[3][1], f"{data[0][2]}, {data[3][2]}")
        right = ("right", data[1][1] + data[2][1], f"{data[1][2]}, {data[2][2]}")
        upper = ("upper", data[2][1] + data[3][1], f"{data[2][2]}, {data[3][2]}")
        lower = ("lower", data[0][1] + data[1][1], f"{data[0][2]}, {data[1][2]}")
        grid.extend(data + [SEPARATING_LINE] + [left, right, upper, lower])
        return tabulate(grid, **self.tb_option, colalign=("global", "center"))

    @property
    def full_report(self) -> str:
        output = "\n"
        for dist in ["element", "quality", "polarity"]:
            output += self.draw_table(
                f"{dist.capitalize()} Distribution ({self.data1.name})",
                self.distribution_table(dist),
            )
        output += self.draw_table(
            f"Celestial Bodies ({self.data1.name})", self.aspectable_body_table
        )
        output += self.draw_table(f"Quadrants ({self.data1.name})", self.quadrant_table)
        output += self.draw_table(f"Houses ({self.data1.name})", self.house_table)
        if self.data2:
            output += self.draw_table(
                f"Celestial Bodies of {self.data2.name} in {self.data1.name}'s chart",
                self.data2_aspectable_body_table,
            )
            output += self.draw_table(
                f"Aspects of {self.data2.name} vs {self.data1.name}",
                self.composite_aspect_table,
            )
            output += self.draw_table(
                f"Aspect Grid of {self.data2.name}(horizontal) vs {self.data1.name}(vertical)",
                self.composite_aspect_grid,
            )
        else:
            output += self.draw_table(f"Aspects ({self.data1.name})", self.aspect_table)
            output += self.draw_table(
                f"Aspect Grid ({self.data1.name})", self.aspect_grid
            )
        return output

    # utils ======================================================================

    def draw_table(self, title: str, table: str) -> str:
        output = f"# {title}\n\n"
        output += table
        output += "\n\n\n"
        return output

    def draw_aspect_table(self, aspects: list[Aspect], headers: list[str]) -> str:
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
        return tabulate(
            grid,
            **self.tb_option,
            colalign=(
                "global",
                "center",
                "global",
                "center",
            ),
        )

    def draw_aspect_grid(self, data1: Data, data2: Data, aspects: list[Aspect]) -> str:
        body_symbols = [body.symbol for body in data1.aspectables]
        grid = [[""] + body_symbols + ["Total"]]  # Header row with Total column
        for body1 in data1.aspectables:
            row = [body1.symbol]
            aspect_count = 0
            for body2 in data2.aspectables:
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

        return tabulate(
            grid, stralign="center", **self.tb_option | {"tablefmt": "simple_grid"}
        )


# for quick testing
if __name__ == "__main__":
    from tests import config, person1, person2

    shing = Data(**person1, config=config)
    belle = Data(**person2, config=config)
    stats = Stats(data1=belle, data2=None)
    print(stats.full_report)
