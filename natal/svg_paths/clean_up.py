"""SVG cleanup script

- optimize SVGs using scour
- clean up unnecessary tags and attributes

Usage:
- export all celestial body SVGs from the Figma file (astrology.fig) to this folder
- run this script in current folder
"""

import re
import subprocess
from pathlib import Path

svgs = Path(__file__).parent.glob("*.svg")

for svg in svgs:
    # use scour to optimize the svg
    cmd = f"scour -i {svg} --enable-id-stripping --enable-comment-stripping --indent=none --strip-xml-prolog --quiet"
    content = subprocess.run(cmd.split(), capture_output=True, text=True).stdout

    # Remove svg tag
    content = re.sub(r"<svg[^>]*>|</svg>", "", content)

    # Remove g tag
    content = re.sub(r"<g[^>]*>|</g>", "", content)

    # Remove fill, stroke and stroke-width attributes
    content = re.sub(r'\s*(fill|stroke|stroke-width)="[^"]*"', "", content)

    # Remove defs tag and its content
    content = re.sub(r"<defs>.*?</defs>", "", content, flags=re.DOTALL)

    # Remove blank lines, including first and last
    content = re.sub(r"^\s*$\n", "", content, flags=re.MULTILINE)

    content = content.strip()

    with svg.open("w") as file:
        file.write(content)
