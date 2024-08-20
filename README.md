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

Creating a natal chart is the foundation of developing astrological software. Traditionally, the Python ecosystem has focused more on the "data" side, such as the calculation of astrological entities (planet positions, house cusps, etc.) but not as much on the "visualization" side, which involves plotting the natal chart in a graphical format. Current tools are outdated, not very Pythonic, and not friendly to code completion or Copilot(as they often present data in generic types eg. str, list, dict...). Not to mention the lack docstrings, examples, and proper documentation.

## Tech Stack

- [kTemplate] for creating and manipulating XML(SVG)
- [pyswisseph] python extension to the Swiss Ephemeris
- [mkdocs-material] for docs site generation

[kTemplate]: https://github.com/hoishing/kTemplate
[pyswisseph]: https://github.com/astrorigin/pyswisseph
[mkdocs-material]: https://github.com/squidfunk/mkdocs-material
[MIT-badge]: https://img.shields.io/github/license/hoishing/natal
[MIT-url]: https://opensource.org/licenses/MIT
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
