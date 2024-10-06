from natal.stats import Stats
from pytest import fixture
from . import data1, data2


@fixture(scope="module")
def stats(data1):
    return Stats(data1=data1)


@fixture(scope="module")
def composite_stats(data1, data2):
    return Stats(data1, data2)


# fmt: off

@fixture
def element_grid():
    return [
        ("element", "count", "bodies"),
        ("earth", 4, "sun ♉, moon ♑, mercury ♉, jupiter ♉"),
        ("fire", 2, "venus ♈, neptune ♐"),
        ("water", 5, "mars ♋, saturn ♋, uranus ♏, mean_node ♏, mc ♋"),
        ("air", 2, "pluto ♎, asc ♎"),
    ]


@fixture
def quality_grid():
    return [
        ("quality", "count", "bodies"),
        ("fixed", 5, "sun ♉, mercury ♉, jupiter ♉, uranus ♏, mean_node ♏"),
        ("cardinal", 7, "moon ♑, venus ♈, mars ♋, saturn ♋, pluto ♎, asc ♎, mc ♋"),
        ("mutable", 1, "neptune ♐"),
    ]


@fixture
def polarity_grid():
    return [
        ("polarity", "count", "bodies"),
        ("negative", 9, "sun ♉, moon ♑, mercury ♉, mars ♋, jupiter ♉, saturn ♋, uranus ♏, mean_node ♏, mc ♋",),
        ("positive", 4, "venus ♈, neptune ♐, pluto ♎, asc ♎"),
    ]


@fixture
def celestial_body_grid():
    return [
        ("body", "sign", "house"),
        ("sun", "00°♉26'", 7),
        ("moon", "19°♑47'", 3),
        ("mercury", "18°♉30'", 7),
        ("venus", "14°♈49'", 6),
        ("mars", "15°♋54'", 9),
        ("jupiter", "05°♉52'", 7),
        ("saturn", "26°♋31'", 10),
        ("uranus", "05°♏19'℞", 1),
        ("neptune", "13°♐38'℞", 2),
        ("pluto", "09°♎47'℞", 12),
        ("mean_node", "13°♏25'℞", 1),
        ("asc", "20°♎32'", 1),
        ("mc", "20°♋36'", 10),
    ]

@fixture
def data2_celestial_body_grid():
    return [
        ("belle", "sign", "house"),
        ("sun", "02°♒38'", 4),
        ("moon", "15°♍46'", 11),
        ("mercury", "12°♑25'", 3),
        ("venus", "16°♐22'", 2),
        ("mars", "05°♒32'", 4),
        ("jupiter", "00°♈03'", 6),
        ("saturn", "17°♎13'", 12),
        ("uranus", "27°♓37'", 6),
        ("neptune", "27°♒26'", 5),
        ("pluto", "06°♑05'", 3),
        ("mean_node", "01°♑08'℞", 3),
        ("asc", "00°♓24'", 5),
        ("mc", "08°♐54'", 2),
    ]

@fixture
def quadrant_grid():
    return [
        ("quadrant", "count", "bodies"),
        ("first", 4, "moon, uranus, neptune, mean_node"),
        ("second", 1, "venus"),
        ("third", 4, "sun, mercury, mars, jupiter"),
        ("fourth", 2, "saturn, pluto"),
    ]

@fixture
def hemisphere_grid():
    return [
        ('hemisphere', 'count', 'bodies'),
        ('eastern', 6, "moon, uranus, neptune, mean_node, saturn, pluto"),
        ('western', 5, "venus, sun, mercury, mars, jupiter"),
        ('northern', 6, "sun, mercury, mars, jupiter, saturn, pluto"),
        ('southern', 5, "moon, uranus, neptune, mean_node, venus"),
    ]

@fixture
def house_grid():
    return [
        ("house", "sign", "ruler", "ruler sign", "ruler house"),
        ("one", "20°♎32'", "venus", "♈ aries", 6),
        ("two", "19°♏43'", "pluto", "♎ libra", 12),
        ("three", "19°♐49'", "jupiter", "♉ taurus", 7),
        ("four", "20°♑36'", "saturn", "♋ cancer", 10),
        ("five", "21°♒53'", "uranus", "♏ scorpio", 1),
        ("six", "22°♓29'", "neptune", "♐ sagittarius", 2),
        ("seven", "20°♈32'", "mars", "♋ cancer", 9),
        ("eight", "19°♉43'", "venus", "♈ aries", 6),
        ("nine", "19°♊49'", "mercury", "♉ taurus", 7),
        ("ten", "20°♋36'", "moon", "♑ capricorn", 3),
        ("eleven", "21°♌54'", "sun", "♉ taurus", 7),
        ("twelve", "22°♍29'", "mercury", "♉ taurus", 7),
    ]


@fixture
def data1_aspect_grid():
    return [
        ["body 1", "aspect", "body 2", "phase", "orb"],
        ("sun", "☌", "jupiter", "> <", "5° 26'"),
        ("sun", "□", "saturn", "<->", "3° 55'"),
        ("sun", "☍", "uranus", "> <", "4° 53'"),
        ("moon", "△", "mercury", "<->", "1° 17'"),
        ("moon", "□", "venus", "<->", "4° 58'"),
        ("moon", "☍", "mars", "<->", "3° 53'"),
        ("moon", "□", "asc", "> <", "0° 45'"),
        ("moon", "☍", "mc", "> <", "0° 49'"),
        ("mercury", "⚹", "mars", "<->", "2° 36'"),
        ("mercury", "☍", "mean_node", "<->", "5° 05'"),
        ("mercury", "⚹", "mc", "> <", "2° 06'"),
        ("venus", "□", "mars", "> <", "1° 05'"),
        ("venus", "△", "neptune", "<->", "1° 11'"),
        ("venus", "☍", "pluto", "<->", "5° 02'"),
        ("venus", "☍", "asc", "> <", "5° 43'"),
        ("venus", "□", "mc", "> <", "5° 47'"),
        ("mars", "△", "mean_node", "<->", "2° 29'"),
        ("mars", "□", "asc", "> <", "4° 38'"),
        ("mars", "☌", "mc", "> <", "4° 42'"),
        ("jupiter", "☍", "uranus", "<->", "0° 34'"),
        ("saturn", "□", "asc", "<->", "5° 59'"),
        ("saturn", "☌", "mc", "<->", "5° 55'"),
        ("neptune", "⚹", "pluto", "<->", "3° 51'"),
        ("asc", "□", "mc", "> <", "0° 04'"),
    ]

@fixture
def composite_aspect_grid():
    return [
        ["belle", "aspect", "shing", "phase", "orb"],
        ("moon", "⚹", "mars", "> <", "0° 08'"),
        ("venus", "△", "venus", "> <", "1° 33'"),
        ("mars", "□", "jupiter", "> <", "0° 20'"),
        ("mars", "□", "uranus", "<->", "0° 13'"),
        ("saturn", "□", "mars", "> <", "1° 18'"),
        ("uranus", "△", "saturn", "> <", "1° 06'"),
        ("pluto", "△", "jupiter", "> <", "0° 13'"),
        ("pluto", "⚹", "uranus", "<->", "0° 46'"),
        ("mean_node", "△", "sun", "> <", "0° 42'"),
        ("asc", "⚹", "sun", "<->", "0° 02'"),
        ("mc", "⚹", "pluto", "> <", "0° 53'"),
    ]



@fixture
def data1_cross_ref_grid():
    return [
        ["", "☉", "☽", "☿", "♀", "♂", "♃", "♄", "♅", "♆", "♇", "☊", "Asc", "MC", "Total"],
        ["☉", "", "", "", "", "", "☌", "□", "☍", "", "", "", "", "", "3"],
        ["☽", "", "", "△", "□", "☍", "", "", "", "", "", "", "□", "☍", "5"],
        ["☿", "", "△", "", "", "⚹", "", "", "", "", "", "☍", "", "⚹", "4"],
        ["♀", "", "□", "", "", "□", "", "", "", "△", "☍", "", "☍", "□", "6"],
        ["♂", "", "☍", "⚹", "□", "", "", "", "", "", "", "△", "□", "☌", "6"],
        ["♃", "☌", "", "", "", "", "", "", "☍", "", "", "", "", "", "2"],
        ["♄", "□", "", "", "", "", "", "", "", "", "", "", "□", "☌", "3"],
        ["♅", "☍", "", "", "", "", "☍", "", "", "", "", "", "", "", "2"],
        ["♆", "", "", "", "△", "", "", "", "", "", "⚹", "", "", "", "2"],
        ["♇", "", "", "", "☍", "", "", "", "", "⚹", "", "", "", "", "2"],
        ["☊", "", "", "☍", "", "△", "", "", "", "", "", "", "", "", "2"],
        ["Asc", "", "□", "", "☍", "□", "", "□", "", "", "", "", "", "□", "5"],
        ["MC", "", "☍", "⚹", "□", "☌", "", "☌", "", "", "", "", "□", "", "6"]
    ]

@fixture
def composite_cross_ref_grid():
    return [
        ['', '☉', '☽', '☿', '♀', '♂', '♃', '♄', '♅', '♆', '♇', '☊', 'Asc', 'MC', 'Total'],
        ['☉', "", "", "", "", "", "", "", "", "", "", '△', '⚹', "", '2'],
        ['☽', "", "", "", "", "", "", "", "", "", "", "", "", "", '0'],
        ['☿', "", "", "", "", "", "", "", "", "", "", "", "", "", '0'],
        ['♀', "", "", "", '△', "", "", "", "", "", "", "", "", "", '1'],
        ['♂', "", '⚹', "", "", "", "", '□', "", "", "", "", "", "", '2'],
        ['♃', "", "", "", "", '□', "", "", "", "", '△', "", "", "", '2'],
        ['♄', "", "", "", "", "", "", "", '△', "", "", "", "", "", '1'],
        ['♅', "", "", "", "", '□', "", "", "", "", '⚹', "", "", "", '2'],
        ['♆', "", "", "", "", "", "", "", "", "", "", "", "", "", '0'],
        ['♇', "", "", "", "", "", "", "", "", "", "", "", "", '⚹', '1'],
        ['☊', "", "", "", "", "", "", "", "", "", "", "", "", "", '0'],
        ['Asc', "", "", "", "", "", "", "", "", "", "", "", "", "", '0'],
        ['MC', "", "", "", "", "", "", "", "", "", "", "", "", "", '0']
    ]

# fmt: on


def test_distribution_grid(stats, element_grid, quality_grid, polarity_grid):
    assert stats.distribution("element").grid == element_grid
    assert stats.distribution("quality").grid == quality_grid
    assert stats.distribution("polarity").grid == polarity_grid


def test_celestial_body_grid(stats, celestial_body_grid):
    assert stats.celestial_body.grid == celestial_body_grid


def test_data2_celestial_body_grid(composite_stats, data2_celestial_body_grid):
    assert composite_stats.data2_celestial_body.grid == data2_celestial_body_grid


def test_quadrant_grid(stats, quadrant_grid):
    assert stats.quadrant.grid == quadrant_grid


def test_hemisphere_grid(stats, hemisphere_grid):
    assert stats.hemisphere.grid == hemisphere_grid


def test_house_grid(stats, house_grid):
    assert stats.house.grid == house_grid


def test_data1_aspect_grid(stats, data1_aspect_grid):
    assert stats.aspect.grid == data1_aspect_grid


def test_composite_aspect_grid(composite_stats, composite_aspect_grid):
    assert composite_stats.composite_aspect.grid == composite_aspect_grid


def test_data1_cross_ref_grid(stats, data1_cross_ref_grid):
    assert stats.cross_ref.grid == data1_cross_ref_grid


def test_composite_cross_ref_grid(composite_stats, composite_cross_ref_grid):
    assert composite_stats.cross_ref.grid == composite_cross_ref_grid
