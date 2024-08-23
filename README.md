# Natal

[![MIT-badge]][MIT-url] [![black-badge]][black-url]

> create Natal Chart in SVG with ease

## Features

- SVG natal chart generation in pure python
- astrological entities in `Enum` to enhance DX
    - better code intellisense
    - more accurate copilot completion
    - enhanced type safety
- high precision astrological data with [Swiss Ephemeris]
- timezone, latitude and longitude database from [GeoNames]
- docstrings with examples
- test with `doctest` and `pytest`

[Swiss Ephemeris]: https://www.astro.com/swisseph/swephinfo_e.htm
[GeoNames]: https://www.geonames.org

## Usage

- installation

`pip install natal`

- quick start

```python
from natal import Astro, Chart

# create object for the natal chart data
natal_data = NatalData(
  name = "Person1",
  yr = 1980, mo = 1, day = 1,
  hr = 12, min = 0,
  city = "Taipei"
)

# return SVG string, optionally export to file
svg = Chart(natal_data, output="./natal-chart.svg")


## -- retrieve natal chart properties -- ##
# houses cusp
natal_data.houses

# aspect(angle) between planets
natal_data.aspects

# percentage of planet in each element(fire, earth, air, water)
natal_data.element_percentage
```

refer the [documentation] for chart configuration and other details

[documentation]: https://hoishing.github.io/natal

## Motivation

Creating a natal chart is fundamental to developing astrological software. Currently, the Python ecosystem:

- Primarily focuses on the "data" aspect of astrological entities, such as calculating planet positions, house cusps, etc.
- Lacks robust visualization tools for rendering natal charts in a graphical format
- The available Python natal charting packages:
    - Are outdated and not very Pythonic (often due to being ported from other languages)
    - Are not friendly to code completion or Copilot (as they frequently use generic types like `str`, `list`, `dict`, etc.)
    - Lack docstrings, examples, and comprehensive documentation

This package aims to address the above problems, and provide a pythonic way to create natal chart.

## Tech Stack

- [ptag] for creating and manipulating XML(SVG)
- [pyswisseph] python extension to the Swiss Ephemeris
- [mkdocs-material] for docs site generation

[ptag]: https://github.com/hoishing/ptag
[pyswisseph]: https://github.com/astrorigin/pyswisseph
[mkdocs-material]: https://github.com/squidfunk/mkdocs-material
[MIT-badge]: https://img.shields.io/github/license/hoishing/natal
[MIT-url]: https://opensource.org/licenses/MIT
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
