from io import BytesIO
from collections import defaultdict
from natal import Chart, Config, Data, Stats
from natal.config import Orb
from natal.const import (
    ASPECT_MEMBERS,
    ELEMENT_MEMBERS,
    EXTRA_MEMBERS,
    PLANET_MEMBERS,
    QUALITY_MEMBERS,
    SIGN_MEMBERS,
    VERTEX_MEMBERS,
)
from natal.stats import StatData, dignity_of
from pathlib import Path
from tagit import div, main, style, svg, table, td, tr
from typing import Iterable
from weasyprint import HTML

Grid = list[Iterable[str | int]]
ELEMENTS = [ELEMENT_MEMBERS[i] for i in (0, 2, 3, 1)]
TEXT_COLOR = "#595959"
symbol_name_map = {
    asp.symbol: asp.name
    for asp in (PLANET_MEMBERS + EXTRA_MEMBERS + VERTEX_MEMBERS + ASPECT_MEMBERS)
}


class Report:
    def __init__(self, data1: Data, data2: Data | None = None):
        self.data1 = data1
        self.data2 = data2

    @property
    def basic_info(self) -> Grid:
        time_fmt = "%Y-%m-%d %H:%M"
        dt1 = self.data1.dt.strftime(time_fmt)
        output = [["name", "city", "birth"]]
        output.append([self.data1.name, self.data1.city, dt1])
        if self.data2:
            dt2 = self.data2.dt.strftime(time_fmt)
            output.append([self.data2.name, self.data2.city, dt2])
        return list(zip(*output))

    @property
    def element_vs_quality(self) -> Grid:
        aspectable1 = self.data1.aspectables
        element_symbols = [svg_of(ele.name) for ele in ELEMENTS]
        grid = [[""] + element_symbols + ["sum"]]
        element_count = defaultdict(int)
        for quality in QUALITY_MEMBERS:
            row = [svg_of(quality.name)]
            quality_count = 0
            for element in ELEMENTS:
                count = 0
                symbols = ""
                for body in aspectable1:
                    if (
                        body.sign.element == element.name
                        and body.sign.quality == quality.name
                    ):
                        symbols += svg_of(body.name)
                        count += 1
                        element_count[element.name] += 1
                row.append(symbols)
                quality_count += count
            row.append(quality_count)
            grid.append(row)
        grid.append(
            ["sum"] + list(element_count.values()) + [sum(element_count.values())]
        )
        grid.append(
            [
                "◐",
                f"null:{element_count['fire'] + element_count['air']} pos",
                f"null:{element_count['water'] + element_count['earth']} neg",
                "",
            ]
        )
        return grid

    @property
    def quadrants_vs_hemisphere(self) -> Grid:
        q = self.data1.quadrants
        first_q = [svg_of(body.name) for body in q[0]]
        second_q = [svg_of(body.name) for body in q[1]]
        third_q = [svg_of(body.name) for body in q[2]]
        forth_q = [svg_of(body.name) for body in q[3]]
        hemi_symbols = ["←", "→", "↑", "↓"]
        grid = [[""] + hemi_symbols[:2] + ["sum"]]
        grid += [["↑"] + [forth_q, third_q] + [len(q[3] + q[2])]]
        grid += [["↓"] + [first_q, second_q] + [len(q[3] + q[2])]]
        grid += [
            ["sum"]
            + [len(q[3] + q[0]), len(q[1] + q[2])]
            + [len(q[0] + q[1] + q[2] + q[3])]
        ]
        return grid

    @property
    def signs(self) -> Grid:
        grid = [["sign", "bodies", "sum"]]
        for sign in SIGN_MEMBERS:
            bodies = [
                svg_of(b.name)
                for b in self.data1.aspectables
                if b.sign.name == sign.name
            ]
            grid.append([svg_of(sign.name), "".join(bodies), len(bodies) or ""])
        return grid

    @property
    def houses(self) -> Grid:
        grid = [["house", "cusp", "bodies", "sum"]]
        for hse in self.data1.houses:
            bodies = [
                svg_of(b.name)
                for b in self.data1.aspectables
                if self.data1.house_of(b) == hse.value
            ]
            grid.append(
                [
                    hse.value,
                    f"{hse.signed_deg:02d}° {svg_of(hse.sign.name)} {hse.minute:02d}'",
                    "".join(bodies),
                    len(bodies) or "",
                ]
            )
        return grid

    @property
    def celestial_body1(self) -> Grid:
        return self.celestial_body(self.data1)

    @property
    def celestial_body2(self) -> Grid:
        return self.celestial_body(self.data2)

    def celestial_body(self, data: Data) -> Grid:
        grid = [("body", "sign", "house", "dignity")]
        for body in data.aspectables:
            grid.append(
                (
                    svg_of(body.name),
                    f"{body.signed_deg:02d}° {svg_of(body.sign.name)} {body.minute:02d}'",
                    self.data1.house_of(body),
                    svg_of(dignity_of(body)),
                )
            )
        return grid

    @property
    def cross_ref(self) -> StatData:
        stats = Stats(self.data1, self.data2)
        grid = stats.cross_ref.grid
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                cell = grid[row][col]
                if name := symbol_name_map.get(cell):
                    grid[row][col] = svg_of(name)
        return StatData(stats.cross_ref.title, grid)

    @property
    def full_report(self) -> str:
        chart = Chart(self.data1, width=400, data2=self.data2)
        row1 = div(
            section("Birth Info", self.basic_info)
            + section("Elements, Modality & Polarity", self.element_vs_quality)
            + section("Hemisphere & Quadrants", self.quadrants_vs_hemisphere),
            class_="info_col",
        ) + div(chart.svg, class_="chart")

        row2 = section(f"{self.data1.name}'s Celestial Bodies", self.celestial_body1)

        if self.data2:
            row2 += section(
                f"{self.data2.name}'s Celestial Bodies", self.celestial_body2
            )
        row2 += section(self.cross_ref.title, self.cross_ref.grid)
        row3 = section("Signs", self.signs) + section("Houses", self.houses)
        css = Path(__file__).parent / "report.css"
        html = style(css.read_text()) + main(
            div(row1, class_="row1")
            + div(row2, class_="row2")
            + div(row3, class_="row3")
        )
        return html

    def create_pdf(self, html: str) -> BytesIO:
        fp = BytesIO()
        HTML(string=html).write_pdf(fp)
        return fp


# utils ======================================================================


def html_table_of(grid: Grid) -> str:
    rows = []
    for row in grid:
        cells = []
        for cell in row:
            if isinstance(cell, str) and cell.startswith("null:"):
                cells.append(td(cell.split(":")[1], colspan=2))
            else:
                cells.append(td(cell))
        rows.append(tr(cells))
    return table(rows)


def svg_of(name: str, scale: float = 0.5) -> str:
    if not name:
        return ""
    stroke = TEXT_COLOR
    fill = "none"
    if name in ["mc", "asc", "dsc", "ic"]:
        stroke = "none"
        fill = TEXT_COLOR

    return svg(
        (Path(__file__).parent / "svg_paths" / f"{name}.svg").read_text(),
        fill=fill,
        stroke=stroke,
        stroke_width=3 * scale,
        version="1.1",
        width=f"{20 * scale}px",
        height=f"{20 * scale}px",
        transform=f"scale({scale})",
        xmlns="http://www.w3.org/2000/svg",
    )


def section(title: str, grid: Grid) -> str:
    return div(
        div(title, class_="title") + html_table_of(grid),
        class_="section",
    )


# sample data ================================================================

if __name__ == "__main__":
    person1 = {
        "name": "Shing",
        "city": "Hong Kong",
        "dt": "1976-04-20 18:58",
    }

    person2 = {
        "name": "Belle",
        "city": "Hong Kong",
        "dt": "2011-01-23 08:44",
    }

    orb = Orb(
        conjunction=2,
        opposition=2,
        trine=2,
        square=2,
        sextile=1,
    )

    data1 = Data(**person1, config=Config(theme_type="light", orb=orb))
    data2 = Data(**person2)
    report = Report(data1, data2)
    fp = report.create_pdf(report.full_report)
    with open("report.pdf", "wb") as f:
        f.write(fp.getvalue())
