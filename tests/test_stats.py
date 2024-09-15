from natal.stats import Stats
from pytest import fixture
from . import data


@fixture(scope="module")
def stats(data):
    return Stats(data=data)


@fixture
def element_table():
    return """\
| element   |   count | bodies                                             |
|-----------+---------+----------------------------------------------------|
| earth     |       4 | sun ♉, moon ♑, mercury ♉, jupiter ♉            |
| fire      |       3 | venus ♈, neptune ♐, chiron ♈                    |
| water     |       5 | mars ♋, saturn ♋, uranus ♏, mean_node ♏, mc ♋ |
| air       |       2 | pluto ♎, asc ♎                                   |"""


@fixture
def quality_table():
    return """\
| quality   |   count | bodies                                                                    |
|-----------+---------+---------------------------------------------------------------------------|
| fixed     |       5 | sun ♉, mercury ♉, jupiter ♉, uranus ♏, mean_node ♏                   |
| cardinal  |       8 | moon ♑, venus ♈, mars ♋, saturn ♋, pluto ♎, chiron ♈, asc ♎, mc ♋ |
| mutable   |       1 | neptune ♐                                                                |"""


@fixture
def polarity_table():
    return """\
| polarity   |   count | bodies                                                                                      |
|------------+---------+---------------------------------------------------------------------------------------------|
| negative   |       9 | sun ♉, moon ♑, mercury ♉, mars ♋, jupiter ♉, saturn ♋, uranus ♏, mean_node ♏, mc ♋ |
| positive   |       5 | venus ♈, neptune ♐, pluto ♎, chiron ♈, asc ♎                                           |"""


@fixture
def aspectable_body_table():
    return """\
| body      | sign      |   house |
|-----------+-----------+---------|
| sun       | 00°♉26'  |       7 |
| moon      | 19°♑47'  |       3 |
| mercury   | 18°♉30'  |       7 |
| venus     | 14°♈49'  |       6 |
| mars      | 15°♋54'  |       9 |
| jupiter   | 05°♉52'  |       7 |
| saturn    | 26°♋31'  |      10 |
| uranus    | 05°♏19'℞ |       1 |
| neptune   | 13°♐38'℞ |       2 |
| pluto     | 09°♎47'℞ |      12 |
| chiron    | 27°♈49'  |       7 |
| mean_node | 13°♏25'℞ |       1 |
| asc       | 20°♎32'  |       1 |
| mc        | 20°♋36'  |      10 |"""


@fixture
def house_table():
    return """\
| house   | sign     | ruler   | ruler sign     |   ruler house |
|---------+----------+---------+----------------+---------------|
| one     | 20°♎32' | venus   | ♈ aries       |             6 |
| two     | 19°♏43' | pluto   | ♎ libra       |            12 |
| three   | 19°♐49' | jupiter | ♉ taurus      |             7 |
| four    | 20°♑36' | saturn  | ♋ cancer      |            10 |
| five    | 21°♒53' | uranus  | ♏ scorpio     |             1 |
| six     | 22°♓29' | neptune | ♐ sagittarius |             2 |
| seven   | 20°♈32' | mars    | ♋ cancer      |             9 |
| eight   | 19°♉43' | venus   | ♈ aries       |             6 |
| nine    | 19°♊49' | mercury | ♉ taurus      |             7 |
| ten     | 20°♋36' | moon    | ♑ capricorn   |             3 |
| eleven  | 21°♌54' | sun     | ♉ taurus      |             7 |
| twelve  | 22°♍29' | mercury | ♉ taurus      |             7 |"""


@fixture
def quadrant_table():
    return """\
| quadrant   | count   | bodies                                                           |
|------------+---------+------------------------------------------------------------------|
| first      | 4       | ☽ moon, ♅ uranus, ♆ neptune, ☊ mean_node                         |
| second     | 1       | ♀ venus                                                          |
| third      | 5       | ☉ sun, ☿ mercury, ♂ mars, ♃ jupiter, ⚷ chiron                    |
| fourth     | 2       | ♄ saturn, ♇ pluto                                                |
| ---        | ---     | ---                                                              |
| left       | 6       | ☽ moon, ♅ uranus, ♆ neptune, ☊ mean_node, ♄ saturn, ♇ pluto      |
| right      | 6       | ♀ venus, ☉ sun, ☿ mercury, ♂ mars, ♃ jupiter, ⚷ chiron           |
| upper      | 7       | ☉ sun, ☿ mercury, ♂ mars, ♃ jupiter, ⚷ chiron, ♄ saturn, ♇ pluto |
| lower      | 5       | ☽ moon, ♅ uranus, ♆ neptune, ☊ mean_node, ♀ venus                |"""


@fixture
def aspect_table():
    return """\
| body 1   | aspect   | body 2    | phase   | orb    |
|----------+----------+-----------+---------+--------|
| sun      | ☌        | jupiter   | > <     | 5° 26' |
| sun      | □        | saturn    | <->     | 3° 55' |
| sun      | ☍        | uranus    | > <     | 4° 53' |
| sun      | ☌        | chiron    | <->     | 2° 37' |
| moon     | △        | mercury   | <->     | 1° 17' |
| moon     | □        | venus     | <->     | 4° 58' |
| moon     | ☍        | mars      | <->     | 3° 53' |
| moon     | ☍        | saturn    | > <     | 6° 44' |
| moon     | □        | asc       | > <     | 0° 45' |
| moon     | ☍        | mc        | > <     | 0° 49' |
| mercury  | ⚹        | mars      | <->     | 2° 36' |
| mercury  | ☍        | mean_node | <->     | 5° 05' |
| mercury  | ⚹        | mc        | > <     | 2° 06' |
| venus    | □        | mars      | > <     | 1° 05' |
| venus    | △        | neptune   | <->     | 1° 11' |
| venus    | ☍        | pluto     | <->     | 5° 02' |
| venus    | ☍        | asc       | > <     | 5° 43' |
| venus    | □        | mc        | > <     | 5° 47' |
| mars     | △        | mean_node | <->     | 2° 29' |
| mars     | □        | asc       | > <     | 4° 38' |
| mars     | ☌        | mc        | > <     | 4° 42' |
| jupiter  | ☍        | uranus    | <->     | 0° 34' |
| saturn   | □        | chiron    | <->     | 1° 18' |
| saturn   | □        | asc       | <->     | 5° 59' |
| saturn   | ☌        | mc        | <->     | 5° 55' |
| neptune  | ⚹        | pluto     | <->     | 3° 51' |
| asc      | □        | mc        | > <     | 0° 04' |"""


def test_distribution_tables(stats, element_table, quality_table, polarity_table):
    assert stats.distribution_table("element") == element_table
    assert stats.distribution_table("quality") == quality_table
    assert stats.distribution_table("polarity") == polarity_table


def test_aspectable_body_table(stats, aspectable_body_table):
    assert stats.aspectable_body_table == aspectable_body_table


def test_house_table(stats, house_table):
    assert stats.house_table == house_table


def test_quadrant_table(stats, quadrant_table):
    assert stats.quadrant_table == quadrant_table


def test_aspect_table(stats, aspect_table):
    assert stats.aspect_table == aspect_table
