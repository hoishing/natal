"""statistics and pdf report for natal charts"""

import logging
from collections import defaultdict
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
from natal.stats import Stats
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


class PDF(Stats):
    """PDF report for a natal chart"""

    @property
    def element_vs_modality(self):
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


class AIContext(Stats):
    """AI context for a natal chart"""

    @property
    def aspect_grid(self) -> list[Iterable]:
        """table of aspects for the primary chart"""
        grid = [["body 1", "aspect", "body 2"]]
        for aspect in self.data1.aspects:
            grid.append([aspect.body1.name, aspect.aspect_member.symbol, aspect.body2.name])
        return grid

    @property
    def synastry_aspect_grid(self) -> list[Iterable]:
        """table of composite aspects between two charts"""
        grid = [[self.data2.name, "aspect", self.data1.name]]
        for aspect in self.synastry_aspects:
            grid.append([aspect.body1.name, aspect.aspect_member.symbol, aspect.body2.name])
        return grid

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
