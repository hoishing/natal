from natal.entity import Entity
from natal.enums import Planets
from pytest import mark


@mark.parametrize(
    "body, degree, retro, expected_dms, expected_sign_dms",
    [
        (Planets.mars, 45.5, True, "15° 30' ℞", "15 ♉ 30 ℞"),
        (Planets.moon, 15.2, False, "15° 12'", "15 ♈ 12"),
        (Planets.moon, 14.99, False, "14° 59'", "14 ♈ 59"),
        # Add more test cases here if needed
    ],
)
def test_entity(
    body,
    degree,
    retro,
    expected_dms,
    expected_sign_dms,
):
    obj = Entity(body, degree, retro)
    assert obj.dms == expected_dms
    assert obj.signed_dms == expected_sign_dms
