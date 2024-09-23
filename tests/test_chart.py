from pytest import fixture
from natal.chart import Chart
from natal.data import Data
from tests import data1, data2
from math import floor


@fixture(scope="module")
def chart(data1, data2):
    return Chart(data1=data1, data2=data2, width=500)


@fixture
def house_vertices():
    return [
        (359, 389),
        (29, 59),
        (59, 90),
        (90, 121),
        (121, 151),
        (151, 179),
        (179, 209),
        (209, 239),
        (239, 270),
        (270, 301),
        (301, 331),
        (331, 359),
    ]


@fixture
def adj_outer_degs():
    return [0, 14, 22, 53, 89, 174, 189, 196, 207, 263, 270, 277, 349]


@fixture
def adj_inner_degs():
    return [3, 23, 32, 195, 226, 277, 286, 297, 306, 315, 329, 338, 353]


def test_house_vertices(chart, house_vertices):
    floor_vertices = [
        tuple(floor(v) for v in vertices) for vertices in chart.house_vertices
    ]
    assert house_vertices == floor_vertices


def test_adjusted_outer_degrees(chart, adj_outer_degs):
    input_degs = sorted(asp.normalized_degree for asp in chart.data1.aspectables)
    adj_degs = chart.adjusted_degrees(input_degs, chart.config.chart.outer_min_degree)
    floor_degs = [floor(d) for d in adj_degs]
    assert floor_degs == adj_outer_degs


def test_adjusted_inner_degrees(chart, adj_inner_degs):
    input_degs = sorted(asp.normalized_degree for asp in chart.data2.aspectables)
    adj_degs = chart.adjusted_degrees(input_degs, chart.config.chart.inner_min_degree)
    floor_degs = [floor(d) for d in adj_degs]
    assert floor_degs == adj_inner_degs


def test_aspect_lines():
    # refer test_data.py -> test_composite_aspects_pairs and test_calculate_aspects
    pass
