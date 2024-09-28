# Natal

[![ci-badge]][ci-url] [![pypi-badge]][pypi-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]

> create SVG natal chart in python with ease

## Features

- SVG natal chart generation in pure python
    - light, dark or auto theme based on user's computer settings
    - printing friednly mono theme
- highly configurable with yaml file
    - all planets, asteroids, vertices can be enabled / disabled
    - orbs for each apect
    - light and dark theme color definitions
    - chart stroke, opacity, font, spacing between planets ...etc
- high precision astrological data with [Swiss Ephemeris]
- timezone, latitude and longitude database from [GeoNames]
    - auto aware of daylight saving for given time and location
- natal chart data statistics
    - element, qauality, and polarity counts
    - planets in each houses
    - aspect pair counts
    - aspects cross reference table
- docs with examples
- tested with `pytest`

## Sample Charts

- default dark theme

<img src="https://bit.ly/4eufbuW" width=600/>

- default light theme

<img src="https://bit.ly/3MT86Zl" width=600/>

- mono theme

<img src="https://bit.ly/3ZygoNw" width=600/>

[Swiss Ephemeris]: https://www.astro.com/swisseph/swephinfo_e.htm
[GeoNames]: https://www.geonames.org

## Quick Start

- installation

`pip install natal`

- generate a chart

```python
from natal import Data, Chart

# create chart data object
mimi = Data(
  name = "MiMi",
  city = "Taipei",
  dt = "1980-04-20 14:30"
)

# return natal chart in SVG string
Chart(mimi, width=600).svg

# create transit data object
current = Data(
  name = "Current",
  city = "Taipei",
  dt = datetime.now()
)

# create a transit chart
transit_chart = Chart(
    data1=mimi, 
    data2=current, 
    width=600
)

# view the composite chart in jupyter notebook
from IPython.display import HTML

HTML(transit_chart.svg)
```

following SVG chart will be produced:

<img src="https://bit.ly/3MX7H8e" width=600/>

## Data Object

```python
## -- retrieve natal chart properties -- ##

mimi.planets     # list[Planet]
mimi.houses      # list[House]
mimi.extras      # list[Extra]
mimi.vertices    # list[Vertex]
mimi.signs       # list[Sign]
mimi.aspects     # list[Aspect]
mimi.quadrants   # list[list[Aspectable]]

# Planet object 
sun = mimi.planets[0]

sun.degree # 30.33039116987769
sun.normalized_degree # 230.62043431588035 # degree relative to Asc
sun.color # fire
sun.speed # 0.9761994105153413
sun.retro # False
sun.dms # 00°19'
sun.signed_dms # 00°♉19'
sun.signed_deg # 0
sun.sign.name # taurus
sun.sign.symbol # ♉
sun.sign.value # 2
sun.sign.color # earth
sun.sign.ruler # venus
sun.sign.classic_ruler # venus
sun.sign.element # earth
sun.sign.quality # fixed
sun.sign.polarity # negative

# Aspect object
aspect = mimi.aspects[0]

aspect.body1 # sun Planet obj 
aspect.body2 # mars Planet obj
aspect.aspect_member # AspectMember(name='trine', symbol='△', value=120, color='air')
aspect.applying # False
aspect.orb # 3.3424
```

## Stats

- statistics of Data object in tabular form

```python
from natal import Data, Stats
from datetime import datetime

mimi = Data(x
    name = "MiMi",
    city = "Taipei",
    dt = "1980-04-20 14:30"
)

current = Data(
    name = "Current",
    city = "Taipei",
    dt = datetime.now()
)

stats = Stats(data1=mimi, data2=current)

print(stats.full_report)
```

- following ascii report will be created
- Note: fonts with double space char support is suggested for better ascii table display eg. `Sarasa Mono TC`

```text

# Element Distribution (MiMi)

| element   |  count  | bodies                                        |
| :-------- | :-----: | :-------------------------------------------- |
| earth     |    4    | sun ♉, jupiter ♍, saturn ♍, asc ♍         |
| water     |    2    | moon ♋, uranus ♏                            |
| fire      |    4    | mercury ♈, mars ♌, neptune ♐, mean_node ♌ |
| air       |    3    | venus ♊, pluto ♎, mc ♊                     |


# Quality Distribution (MiMi)

| quality   |  count  | bodies                                                     |
| :-------- | :-----: | :--------------------------------------------------------- |
| fixed     |    4    | sun ♉, mars ♌, uranus ♏, mean_node ♌                   |
| cardinal  |    3    | moon ♋, mercury ♈, pluto ♎                              |
| mutable   |    6    | venus ♊, jupiter ♍, saturn ♍, neptune ♐, asc ♍, mc ♊ |


# Polarity Distribution (MiMi)

| polarity   |  count  | bodies                                                                   |
| :--------- | :-----: | :----------------------------------------------------------------------- |
| negative   |    6    | sun ♉, moon ♋, jupiter ♍, saturn ♍, uranus ♏, asc ♍                |
| positive   |    7    | mercury ♈, venus ♊, mars ♌, neptune ♐, pluto ♎, mean_node ♌, mc ♊ |


# Celestial Bodies (MiMi)

| body      | sign      |  house  |
| :-------- | :-------- | :-----: |
| sun       | 00°♉19'  |    8    |
| moon      | 08°♋29'  |   10    |
| mercury   | 08°♈28'  |    8    |
| venus     | 15°♊12'  |   10    |
| mars      | 26°♌59'  |   12    |
| jupiter   | 00°♍17'℞ |   12    |
| saturn    | 21°♍03'℞ |    1    |
| uranus    | 24°♏31'℞ |    3    |
| neptune   | 22°♐29'℞ |    4    |
| pluto     | 20°♎06'℞ |    2    |
| mean_node | 26°♌03'℞ |   12    |
| asc       | 09°♍42'  |    1    |
| mc        | 09°♊13'  |   10    |


# Houses (MiMi)

| house   | sign     | ruler   | ruler sign     |  ruler house  |
| :------ | :------- | :------ | :------------- | :-----------: |
| one     | 09°♍41' | mercury | ♈ aries       |       8       |
| two     | 07°♎13' | venus   | ♊ gemini      |      10       |
| three   | 07°♏38' | pluto   | ♎ libra       |       2       |
| four    | 09°♐13' | jupiter | ♍ virgo       |      12       |
| five    | 10°♑25' | saturn  | ♍ virgo       |       1       |
| six     | 10°♒44' | uranus  | ♏ scorpio     |       3       |
| seven   | 09°♓41' | neptune | ♐ sagittarius |       4       |
| eight   | 07°♈13' | mars    | ♌ leo         |      12       |
| nine    | 07°♉38' | venus   | ♊ gemini      |      10       |
| ten     | 09°♊13' | mercury | ♈ aries       |       8       |
| eleven  | 10°♋25' | moon    | ♋ cancer      |      10       |
| twelve  | 10°♌44' | sun     | ♉ taurus      |       8       |


# Quadrants (MiMi)

| quadrant   |  count  | bodies                                          |
| :--------- | :-----: | :---------------------------------------------- |
| first      |    3    | ♄ saturn, ♅ uranus, ♇ pluto                     |
| second     |    1    | ♆ neptune                                       |
| third      |    3    | ☉ sun, ☿ mercury, ⚷ chiron                      |
| fourth     |    5    | ☽ moon, ♀ venus, ♂ mars, ♃ jupiter, ☊ mean_node |


# Hemispheres (MiMi)

| hemisphere   |  count  | bodies                                                                       |
| :----------- | :-----: | :--------------------------------------------------------------------------- |
| eastern      |    8    | ♄ saturn, ♅ uranus, ♇ pluto, ☽ moon, ♀ venus, ♂ mars, ♃ jupiter, ☊ mean_node |
| western      |    4    | ♆ neptune, ☉ sun, ☿ mercury, ⚷ chiron                                        |
| northern     |    8    | ☉ sun, ☿ mercury, ⚷ chiron, ☽ moon, ♀ venus, ♂ mars, ♃ jupiter, ☊ mean_node  |
| southern     |    4    | ♄ saturn, ♅ uranus, ♇ pluto, ♆ neptune                                       |


# Celestial Bodies of Current in MiMi's chart

| Current   | sign      |  house  |
| :-------- | :-------- | :-----: |
| sun       | 01°♎05'  |    1    |
| moon      | 16°♊47'  |   10    |
| mercury   | 25°♍01'  |    1    |
| venus     | 00°♏38'  |    2    |
| mars      | 10°♋53'  |   11    |
| jupiter   | 20°♊55'  |   10    |
| saturn    | 14°♓52'℞ |    7    |
| uranus    | 27°♉03'℞ |    9    |
| neptune   | 28°♓26'℞ |    7    |
| pluto     | 29°♑43'℞ |    5    |
| mean_node | 06°♈45'℞ |    7    |
| asc       | 05°♋23'  |   10    |
| mc        | 23°♓43'  |    7    |


# Aspects of Current vs MiMi

| Current   |  aspect  | MiMi      |  phase  | orb    |
| :-------- | :------: | :-------- | :-----: | :----- |
| moon      |    ☌     | venus     |   <->   | 1° 35' |
| mercury   |    ⚹     | uranus    |   <->   | 0° 30' |
| venus     |    ☍     | sun       |   <->   | 0° 19' |
| venus     |    ⚹     | jupiter   |   <->   | 0° 21' |
| jupiter   |    □     | saturn    |   > <   | 0° 08' |
| jupiter   |    ☍     | neptune   |   > <   | 1° 33' |
| jupiter   |    △     | pluto     |   <->   | 0° 49' |
| saturn    |    □     | venus     |   <->   | 0° 20' |
| uranus    |    □     | mars      |   > <   | 0° 04' |
| uranus    |    □     | mean_node |   <->   | 1° 00' |
| pluto     |    □     | sun       |   <->   | 0° 37' |
| mean_node |    □     | moon      |   <->   | 1° 44' |
| mean_node |    ☌     | mercury   |   <->   | 1° 43' |
| mc        |    △     | uranus    |   > <   | 0° 47' |
| mc        |    □     | neptune   |   <->   | 1° 15' |


# Aspect Cross Reference of Current(cols) vs MiMi(rows)

┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬───────┬──────┬─────────┐
│     │  ☉  │  ☽  │  ☿  │  ♀  │  ♂  │  ♃  │  ♄  │  ♅  │  ♆  │  ♇  │  ☊  │  Asc  │  MC  │  Total  │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ☉  │     │     │     │  ☍  │     │     │     │     │     │  □  │     │       │      │    2    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ☽  │     │     │     │     │     │     │     │     │     │     │  □  │       │      │    1    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ☿  │     │     │     │     │     │     │     │     │     │     │  ☌  │       │      │    1    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ♀  │     │  ☌  │     │     │     │     │  □  │     │     │     │     │       │      │    2    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ♂  │     │     │     │     │     │     │     │  □  │     │     │     │       │      │    1    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ♃  │     │     │     │  ⚹  │     │     │     │     │     │     │     │       │      │    1    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ♄  │     │     │     │     │     │  □  │     │     │     │     │     │       │      │    1    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ♅  │     │     │  ⚹  │     │     │     │     │     │     │     │     │       │  △   │    2    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ♆  │     │     │     │     │     │  ☍  │     │     │     │     │     │       │  □   │    2    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ♇  │     │     │     │     │     │  △  │     │     │     │     │     │       │      │    1    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│  ☊  │     │     │     │     │     │     │     │  □  │     │     │     │       │      │    1    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│ Asc │     │     │     │     │     │     │     │     │     │     │     │       │      │    0    │
├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┼──────┼─────────┤
│ MC  │     │     │     │     │     │     │     │     │     │     │     │       │      │    0    │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴───────┴──────┴─────────┘

```

## Configuration

- create a `natal_config.yml` file in project root to override the defaults in `config.py`
- a sample config as follow:

```yaml
theme_type: light

light_theme:
    fire: "#ff0000"
    earth: "#ffff00"
    air: "#00ff00"
    water: "#0000ff"
    points: "#00ffff"

display:
    mean_node: True
    chiron: True

orb:
    conjunction: 8
    opposition: 8
    trine: 6
    square: 6
    sextile: 6
```

read the [docs] for complete references

[docs]: https://hoishing.github.io/natal

## Tech Stack

- [ptag] for creating and manipulating XML(SVG)
- [pyswisseph] python extension to the Swiss Ephemeris
- [mkdocs-material] for docs site generation

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[ci-badge]: https://github.com/hoishing/natal/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/hoishing/natal/actions/workflows/ci.yml
[MIT-badge]: https://img.shields.io/github/license/hoishing/natal
[MIT-url]: https://opensource.org/licenses/MIT
[mkdocs-material]: https://github.com/squidfunk/mkdocs-material
[ptag]: https://github.com/hoishing/ptag
[pypi-badge]: https://img.shields.io/pypi/v/natal
[pypi-url]: https://pypi.org/project/natal
[pyswisseph]: https://github.com/astrorigin/pyswisseph
