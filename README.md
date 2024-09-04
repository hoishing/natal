# Natal

[![MIT-badge]][MIT-url] [![black-badge]][black-url]

> create Natal Chart in SVG with ease

## Features

- SVG natal chart generation in pure python
- high precision astrological data with [Swiss Ephemeris]
- timezone, latitude and longitude database from [GeoNames]
- docs with examples
- tested with `pytest`

[Swiss Ephemeris]: https://www.astro.com/swisseph/swephinfo_e.htm
[GeoNames]: https://www.geonames.org

## Usage

- installation

`pip install natal`

- quick start

```python
from natal import Data, Chart

# create object for the natal chart data
natal_data = Data(
  name = "MiMi",
  city = "Taipei",
  dt = "1980-04-20 14:30"
)

# return SVG string, optionally export to file
svg = Chart(natal_data, output="./natal-chart.svg")


## -- retrieve natal chart properties -- ##
# houses cusp
natal_data.houses

# aspect(angle) between planets
natal_data.aspects

# statistics
...
```

read the [docs] for chart configuration and other details

[docs]: https://hoishing.github.io/natal

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
