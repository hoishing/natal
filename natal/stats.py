"""statistics and pdf report for natal charts"""

import logging
from collections import defaultdict
from dataclasses import dataclass
from io import BytesIO
from natal import Chart
from natal.classes import Aspect, Aspectable
from natal.const import (
    ASPECT_MEMBERS,
    ELEMENT_MEMBERS,
    EXTRA_MEMBERS,
    MODALITY_MEMBERS,
    PLANET_MEMBERS,
    SIGN_MEMBERS,
    VERTEX_MEMBERS,
)
from natal.data import BodyPairs, Data
from pathlib import Path
from tagit import div, main, style, svg, table, td, tr
from typing import Iterable, Literal
from weasyprint import HTML
from zoneinfo import ZoneInfo

# suppress fontTools warnings
logging.getLogger("fontTools").setLevel(logging.ERROR)

DistKind = Literal["element", "modality", "polarity"]
ReportKind = Literal["markdown", "html"]
ELEMENTS = [ELEMENT_MEMBERS[i] for i in (0, 2, 3, 1)]
TEXT_COLOR = "#595959"
symbol_name_map = {
    asp.symbol: asp.name
    for asp in (PLANET_MEMBERS + EXTRA_MEMBERS + VERTEX_MEMBERS + ASPECT_MEMBERS)
}


@dataclass
class Stats:
    """statistics for a natal chart data"""

    data1: Data
    city1: str | None = None
    tz1: str | None = None
    data2: Data | None = None
    city2: str | None = None
    tz2: str | None = None

    composite_pairs: BodyPairs | None = None
    composite_aspects: list[Aspect] | None = None

    def __post_init__(self):
        """setup composite pairs and aspects"""
        if self.data2:
            self.composite_pairs = self.data2.composite_aspects_pairs(self.data1)
            self.composite_aspects = self.data1.calculate_aspects(self.composite_pairs)

    # data grids =================================================================

    @property
    def basic_info(self) -> list[Iterable]:
        """table containing name, city, coordinates, and local birth datetime"""
        time_fmt = "%Y-%m-%d %H:%M"
        dt1 = self.data1.utc_dt.astimezone(ZoneInfo(self.tz1)).strftime(time_fmt)
        coordinates1 = f"{self.data1.lat}°N {self.data1.lon}°E"
        output = [["name", "city", "coordinates", "local time"]]
        output.append([self.data1.name, self.city1, coordinates1, dt1])
        if self.data2:
            dt2 = self.data2.utc_dt.astimezone(ZoneInfo(self.tz2)).strftime(time_fmt)
            coordinates2 = f"{self.data2.lat}°N {self.data2.lon}°E"
            output.append([self.data2.name, self.city2, coordinates2, dt2])
        return list(zip(*output))

    @property
    def element_vs_modality(self) -> list[Iterable]:
        """table of celestial bodies' elements and modalities"""
        aspectable1 = self.data1.aspectables
        element_symbols = [svg_symbol(ele.name) for ele in ELEMENTS]
        grid = [[""] + element_symbols + ["sum"]]
        element_count = defaultdict(int)
        for modality in MODALITY_MEMBERS:
            row = [svg_symbol(modality.name)]
            modality_count = 0
            for element in ELEMENTS:
                count = 0
                symbols = ""
                for body in aspectable1:
                    if body.sign.element == element.name and body.sign.modality == modality.name:
                        symbols += svg_symbol(body.name)
                        count += 1
                        element_count[element.name] += 1
                row.append(symbols)
                modality_count += count
            row.append(modality_count)
            grid.append(row)
        grid.append(["sum"] + list(element_count.values()) + [sum(element_count.values())])
        grid.append(
            [
                "◐",  # symbol of polarity
                f"null:{element_count['fire'] + element_count['air']} pos",
                f"null:{element_count['water'] + element_count['earth']} neg",
                "",
            ]
        )
        return grid

    @property
    def quadrants_vs_hemisphere(self) -> list[Iterable]:
        """table of celestial bodies' quadrants and hemispheres"""
        q = self.data1.quadrants
        first_q = [svg_symbol(body.name) for body in q[0]]
        second_q = [svg_symbol(body.name) for body in q[1]]
        third_q = [svg_symbol(body.name) for body in q[2]]
        forth_q = [svg_symbol(body.name) for body in q[3]]
        hemi_symbols = ["eastern", "western", "northern", "southern"]
        grid = [[""] + hemi_symbols[:2] + ["sum"]]
        grid += [["northern"] + [forth_q, third_q] + [len(q[3] + q[2])]]
        grid += [["southern"] + [first_q, second_q] + [len(q[3] + q[2])]]
        grid += [["sum"] + [len(q[3] + q[0]), len(q[1] + q[2])] + [len(q[0] + q[1] + q[2] + q[3])]]
        return grid

    @property
    def celestial_body1(self) -> list[Iterable]:
        return self.celestial_body(self.data1)

    @property
    def celestial_body2(self) -> list[Iterable]:
        return self.celestial_body(self.data2)

    def celestial_body(self, data: Data) -> list[Iterable]:
        """table of celestial bodies for the given data"""

        grid = [("body", "sign", "house", "dignity")]
        for body in data.aspectables:
            grid.append(
                (
                    svg_symbol(body.name),
                    f"{body.signed_deg:02d}° {svg_symbol(body.sign.name)} {body.minute:02d}'",
                    self.data1.house_of(body),
                    svg_symbol(dignity_of(body)),
                )
            )
        return grid

    @property
    def signs(self) -> list[Iterable]:
        """table of celestial bodies' signs"""
        grid = [["sign", "bodies", "sum"]]
        for sign in SIGN_MEMBERS:
            bodies = [
                svg_symbol(b.name) for b in self.data1.aspectables if b.sign.name == sign.name
            ]
            grid.append([svg_symbol(sign.name), "".join(bodies), len(bodies) or ""])
        return grid

    @property
    def houses(self) -> list[Iterable]:
        """table of celestial bodies' houses"""
        grid = [["house", "cusp", "bodies", "sum"]]
        for hse in self.data1.houses:
            bodies = [
                svg_symbol(b.name)
                for b in self.data1.aspectables
                if self.data1.house_of(b) == hse.value
            ]
            grid.append(
                [
                    hse.value,
                    f"{hse.signed_deg:02d}° {svg_symbol(hse.sign.name)} {hse.minute:02d}'",
                    "".join(bodies),
                    len(bodies) or "",
                ]
            )
        return grid

    @property
    def aspect(self) -> list[Iterable]:
        """table of aspects for the primary chart"""
        grid = [["body 1", "aspect", "body 2"]]
        for aspect in self.data1.aspects:
            grid.append([aspect.body1.name, aspect.aspect_member.symbol, aspect.body2.name])
        return grid

    @property
    def composite_aspect(self) -> list[Iterable]:
        """table of composite aspects between two charts"""
        grid = [[self.data2.name, "aspect", self.data1.name]]
        for aspect in self.composite_aspects:
            grid.append([aspect.body1.name, aspect.aspect_member.symbol, aspect.body2.name])
        return grid

    @property
    def cross_ref(self) -> list[Iterable]:
        """table of aspect cross-reference between charts or within a single chart"""
        aspectable1 = self.data1.aspectables
        aspectable2 = self.data2.aspectables if self.data2 else self.data1.aspectables
        aspects = self.composite_aspects if self.data2 else self.data1.aspects
        body_symbols = [body.symbol for body in aspectable2]
        grid: list[list[str]] = [[""] + body_symbols + ["sum"]]
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
                    row.append("")

            row.append(str(aspect_count))  # Add sum to the end of the row
            grid.append(row)
        return grid

    @property
    def orbs(self) -> list[Iterable]:
        """table of orbs settings"""
        orb = self.data1.config.orb
        return [["aspect", "orb"]] + [[svg_symbol(aspect), orb[aspect]] for aspect in orb]

    @property
    def html_report(self) -> str:
        """full HTML astrological report"""
        output = html_section("Birth Info", self.basic_info)
        output += html_section("Elements, Modality & Polarity", self.element_vs_modality)
        output += html_section("Hemisphere & Quadrants", self.quadrants_vs_hemisphere)
        output += html_section(f"{self.data1.name}'s Celestial Bodies", self.celestial_body1)

        if self.data2:
            output += html_section(f"{self.data2.name}'s Celestial Bodies", self.celestial_body2)
            output += html_section(
                f"Aspects of {self.data2.name} vs {self.data1.name}", self.composite_aspect
            )
        else:
            output += html_section(f"Aspects ({self.data1.name})", self.aspect)

        ref_name = (
            f"{self.data2.name}(cols) vs {self.data1.name}(rows)" if self.data2 else self.data1.name
        )
        ref_title = f"Aspect Cross Reference of {ref_name}"
        output += html_section(ref_title, self.cross_ref)
        output += html_section("Signs", self.signs)
        output += html_section("Houses", self.houses)
        return output

    @property
    def pdf_report(self) -> str:
        """html source for PDF report"""
        chart = Chart(self.data1, width=400, data2=self.data2)
        row1 = div(
            html_section("Birth Info", self.basic_info)
            + html_section("Elements, Modality & Polarity", self.element_vs_modality)
            + html_section("Hemisphere & Quadrants", self.quadrants_vs_hemisphere),
            class_="info_col",
        ) + div(chart.svg, class_="chart")

        row2 = html_section(f"{self.data1.name}'s Celestial Bodies", self.celestial_body1)

        if self.data2:
            row2 += html_section(f"{self.data2.name}'s Celestial Bodies", self.celestial_body2)
        ref_name = (
            f"{self.data2.name}(cols) vs {self.data1.name}(rows)" if self.data2 else self.data1.name
        )
        ref_title = f"Aspect Cross Reference of {ref_name}"
        row2 += html_section(ref_title, self.cross_ref)
        row3 = (
            html_section("Signs", self.signs)
            + html_section("Houses", self.houses)
            + html_section("Orbs", self.orbs)
        )
        css = Path(__file__).parent / "pdf.css"
        html = style(css.read_text()) + main(
            div(row1, class_="row1") + div(row2, class_="row2") + div(row3, class_="row3")
        )
        return html

    def create_pdf(self, html: str) -> BytesIO:
        """Creates a PDF from the given HTML string"""
        fp = BytesIO()
        HTML(string=html).write_pdf(fp)
        return fp

    def ai_md(
        self,
        fn_name: str,
    ) -> str:
        """markdown data for AI context"""
        stat = getattr(self, fn_name)
        rows = stat.grid
        output = f"# {stat.title}\n\n"
        header = rows.pop(0)
        output += "|"
        for item in header:
            output += f"{item} | "
        output += "\n"
        output += "|" + "--- | " * len(header)
        output += "\n"
        for row in rows:
            output += "|"
            for item in row:
                output += f"{item} | "
            output += "\n"
        output += "\n\n"
        return output


# utils ======================================================================


def dignity_of(body: Aspectable) -> str:
    """get the dignity of a celestial body"""
    if body.name == (body.sign.classic_ruler or body.sign.ruler):
        return "domicile"
    if body.name == (body.sign.classic_detriment or body.sign.detriment):
        return "detriment"
    if body.name == body.sign.exaltation:
        return "exaltation"
    if body.name == body.sign.fall:
        return "fall"
    return ""


def html_table(grid: list[Iterable]) -> str:
    """converts list of iterable into an HTML table"""
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


def svg_symbol(name: str, scale: float = 0.5) -> str:
    """generates an SVG tag of a given symbol name"""
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


def html_section(title: str, grid: list[Iterable]) -> str:
    """creates an HTML section with a title and data table"""
    return div(
        div(title, class_="title") + html_table(grid),
        class_="section",
    )
