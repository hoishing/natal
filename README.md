# Natal

> create astrological Natal Chart with ease

## Features

- SVG natal chart generation in pure python
- astrological entities in `Enum` to enhance DX
  - better code intellisense
  - more accurate copilot completion
  - enhanced type safety
- high precision astrological data with [Swiss Ephemeris]
- timezone, latitude and longitude database from [GeoNames]
- docstring with examples
- test with `doctest` and pytest

[Swiss Ephemeris]: https://www.astro.com/swisseph/swephinfo_e.htm

## Usage

- installation

`pip install natal`

- quick start

```python
from natal import Astro, Chart

# create object for the natal chart info
natal_info = Natal(
  name = "Kelvin",
  yr = 1976, mo = 4, day = 20,
  hr = 18, min = 58,
  city = "Taipei"
)

# return SVG string, optionally export to file
svg = Chart(natal_info, output="./natal-chart.svg")


## -- retrieve natal chart properties -- ##
# houses curp
natal_info.houses

# aspect(angle) between planets
natal_info.aspects

# percentage of planet in each element(fire, earth, air, water)
natal_info.element_percentage
```

refer the [documentation] for chart configuration and other details

## Motivation

Creating a natal chart is the foundation of developing astrological software. Traditionally, the Python ecosystem has focused more on the "data" side, such as the calculation of astrological entities (planet positions, house cusps, etc.) but not as much on the "visualization" side, which involves plotting the natal chart in a graphical format. Current tools are outdated, not very Pythonic, and not friendly to code completion or Copilot(as they often present data in generic types eg. str, list, dict...). Not to mention the lack docstrings, examples, and proper documentation.

## Tech Stack

- [Dominate] for creating and manipulating XML(SVG)
- [pyswisseph] python extension to the Swiss Ephemeris
- [mkdocs-material] for docs site generation

[Dominate]: https://github.com/Knio/dominate
[pyswisseph]: https://github.com/astrorigin/pyswisseph
[mkdocs-material]: https://github.com/squidfunk/mkdocs-material
