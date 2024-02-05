"""pytests for noaa.py"""

import pytest
import datetime
from pysunnoaa import noaa

def almostequal(first, second, places=7, printit=True):
    """docstring for almostequal
    # taken from python's unit test
    # may be covered by Python's license

    """
    if round(abs(second - first), places) != 0:
        if printit:
            print(round(abs(second - first), places))
            print("notalmost: %s != %s" % (first, second))
        return False
    else:
        return True

@pytest.mark.parametrize(
    "a, expected",
    [
    (2, 4), # a, expected
    ]
)
def test_add2(a, expected):
    result = noaa.add2(a)
    result == expected

@pytest.mark.parametrize(
    "dt, timezone, expected",
    [
    (datetime.datetime(2010, 6, 21, 0, 6), -6, 2455368.75416667), # dt, timezone, expected
    (datetime.datetime(2023, 9, 21, 5, 33), -8, 2460209.06458333), # dt, timezone, expected
    ],
)
def test_julianday(dt, timezone, expected):
    result = noaa.julianday(dt, timezone)
    assert almostequal(result, expected)

@pytest.mark.parametrize(
    "jul_day, expected",
    [
    (2455368.75416667, 0.104688683550086), # jul_day, expected
    (2460209.06458333, 0.237209160392435), # jul_day, expected
    ]
)
def test_juliancentury(jul_day, expected):
    result = noaa.juliancentury(jul_day)
    assert almostequal(result, expected)

@pytest.mark.parametrize(
    "jul_century, expected",
    [
    (0.104688683550086, 89.3396636153339), # jul_century, expected
    (0.237209160392435, 180.178861916105), # jul_century, expected
    ]
)
def test_geom_mean_long_sun_deg(jul_century, expected):
    result = noaa.geom_mean_long_sun_deg(jul_century)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "jul_century, expected",
    [
    (0.104688683550086, 4126.22229222893), # jul_century, expected
    (0.23720916, 8896.83359556751), # jul_century, expected
    ]
)
def test_geom_mean_anom_sun_deg(jul_century, expected):
    result = noaa.geom_mean_anom_sun_deg(jul_century)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "jul_century, expected",
    [
    (0.104688683550086, 0.016704231813213), # jul_century, expected
    (0.23720916, 0.0166986553093454), # jul_century, expected
    ]
)
def test_ent_earth_orbit(jul_century, expected):
    result = noaa.eccent_earth_orbit(jul_century)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "jul_century, geom_mean_anom_sun_value, expected",
    [
    (0.104689824321243, 4126.22229222893, 0.446799918175887), # jul_century, geom_mean_anom_sun_value, expected
    (0.237209160392435, 8896.83359556751, -1.85407782292307), # jul_century, geom_mean_anom_sun_value, expected
    ]
)
def test_sun_eq_of_ctr(jul_century, geom_mean_anom_sun_value, expected):
    result = noaa.sun_eq_of_ctr(jul_century, geom_mean_anom_sun_value)
    almostequal(result, expected)
