"""SVG cleanup script

- remove svg and g tags
- remove fill, stroke and stroke-width attributes
- remove defs tag and its content
- remove blank lines, including first and last

Usage: 
- export all celestial body SVGs from figma to this folder
- run this script in current folder
"""


from pathlib import Path
import re

svgs = Path(__file__).parent.glob("*.svg")

for svg in svgs:
    with svg.open('r') as file:
        content = file.read()

    # Remove svg tag
    content = re.sub(r'<svg[^>]*>|</svg>', '', content)

    # Remove g tag
    content = re.sub(r'<g[^>]*>|</g>', '', content)

    # Remove fill, stroke and stroke-width attributes
    content = re.sub(r'\s*(fill|stroke|stroke-width)="[^"]*"', '', content)

    # Remove defs tag and its content
    content = re.sub(r'<defs>.*?</defs>', '', content, flags=re.DOTALL)

    # Remove blank lines, including first and last
    content = re.sub(r'^\s*$\n', '', content, flags=re.MULTILINE)
    content = content.strip()

    with svg.open('w') as file:
        file.write(content)