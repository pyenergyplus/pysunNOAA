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
    "dt, expected",
    [
    (datetime.datetime(2001, 10, 2, 5, 30, 35), datetime.datetime(2001, 10, 2)), # dt, expected
    ]
)
def test_datetime_midnight(dt, expected):
    result = noaa.datetime_midnight(dt)
    assert result == expected

@pytest.mark.parametrize(
    "dayfraction, datetime_day, expected",
    [
    (0.25, datetime.datetime(2001, 10, 5, 10, 5), datetime.datetime(2001, 10, 5, 6)), # dayfraction, datetime_day, expected
    (0.25, None, datetime.datetime(2001, 1, 1, 6)), # dayfraction, datetime_day, expected
    (1 / 24 * 14, datetime.datetime(2001, 10, 5, 10, 5), datetime.datetime(2001, 10, 5, 14)), # dayfraction, datetime_day, expected
    ])
def test_dayfraction2datetime(dayfraction, datetime_day, expected):
    result = noaa.dayfraction2datetime(dayfraction, datetime_day)
    assert result == expected

@pytest.mark.parametrize(
    "dayfraction, datetime_day, t_format, expected",
    [
    (0.25, None, None, "06:00:00"), # dayfraction, datetime_day, t_format, expected
    (0.25, None, "%H|%M|%S", "06|00|00"), # dayfraction, datetime_day, t_format, expected
    (0.25, datetime.datetime(1900, 2, 3), "%H|%M|%S", "06|00|00"), # dayfraction, datetime_day, t_format, expected
    ]
)
def test_dayfraction2dateformat(dayfraction, datetime_day, t_format, expected):
    result = noaa.dayfraction2dateformat(dayfraction, datetime_day, t_format)
    assert result == expected

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

@pytest.mark.parametrize(
    "geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected",
    [
    (89.3396636153339, 0.446799918175887, 89.7864635335097), # geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected
    (180.178861916105, -1.85407782292307, 178.324784093182), # geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected
    ]
)
def test_sun_true_long_deg(geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected):
    result = noaa.sun_true_long_deg(geom_mean_long_sun_deg_value, sun_eq_of_ctr_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected",
    [
    (4126.22229222893, 0.446799918175887, 4126.6690921471), # geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected
    (8896.83359556751, -1.85407782292307, 8894.97951774459), # geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected
    ]
)
def test_sun_true_anom_deg(geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected):
    result = noaa.sun_true_anom_deg(geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "eccent_earth_orbit_value, sun_true_anom_deg_value, expected",
    [
    (0.016704231813213, 4126.6690921471, 1.01624008495444), # eccent_earth_orbit_value, sun_true_anom_deg_value, expected
    (0.0166986553093454, 8894.97951774459, 1.0040674712274), # eccent_earth_orbit_value, sun_true_anom_deg_value, expected
    ]
)
def test_sun_rad_vector_AUs(eccent_earth_orbit_value, sun_true_anom_deg_value, expected):
    result = noaa. sun_rad_vector_AUs(eccent_earth_orbit_value, sun_true_anom_deg_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "juliancentury_value, sun_true_long_deg_value, expected",
    [
    (0.10468868, 89.7864635335097, 89.7854391814863), # juliancentury_value, sun_true_long_deg_value, expected
    (0.23720916, 178.324784093182, 178.316980310654), # juliancentury_value, sun_true_long_deg_value, expected
    ]
)
def test_sun_app_long_deg(juliancentury_value, sun_true_long_deg_value, expected):
    result = noaa.sun_app_long_deg(juliancentury_value, sun_true_long_deg_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
    (0.10468868, 23.4379297208038), # juliancentury_value, expected
    (0.23720916, 23.4362064011546), # juliancentury_value, expected
    ]
)
def test_mean_obliq_ecliptic_deg(juliancentury_value, expected):
    result = noaa.mean_obliq_ecliptic_deg(juliancentury_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "juliancentury_value, mean_obliq_ecliptic_deg_value, expected",
    [
    (0.10468868, 23.4379297208038, 23.4384863293544), # juliancentury_value, mean_obliq_ecliptic_deg_value, expected
    (0.23720916, 23.4362064011546, 23.4385024897594), # juliancentury_value, mean_obliq_ecliptic_deg_value, expected
    ]
)
def test_obliq_corr_deg(juliancentury_value, mean_obliq_ecliptic_deg_value, expected):
    result = noaa.obliq_corr_deg(juliancentury_value, mean_obliq_ecliptic_deg_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected",
    [
    (89.7854391814863, 23.4384863293544, 89.7661433042803), # sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected
    (178.316980310654, 23.4385024897594, 178.455780149553), # sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected
    ]
)
def test_sun_rt_ascen_deg(sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected):
    print(sun_app_long_deg_value, mean_obliq_ecliptic_deg_value)
    result = noaa.sun_rt_ascen_deg(sun_app_long_deg_value, mean_obliq_ecliptic_deg_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "sun_app_long_deg_value, obliq_corr_deg_value, expected",
    [
    (89.7854391814863, 23.4384863293544, 23.4383121595139), # sun_app_long_deg_value, obliq_corr_deg_value, expected
    (178.316980310654, 23.4385024897594, 0.66936449061751), # sun_app_long_deg_value, obliq_corr_deg_value, expected
    ]
)
def test_sun_declin_deg(sun_app_long_deg_value, obliq_corr_deg_value, expected):
    result = noaa.sun_declin_deg(sun_app_long_deg_value, obliq_corr_deg_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "obliq_corr_deg_value, expected",
    [
    (23.4384863293544, 0.0430314901072543), # obliq_corr_deg_value, expected
    (23.4385024897594, 0.0430315511340247), # obliq_corr_deg_value, expected
    ]
)
def test_var_y(obliq_corr_deg_value, expected):
    result = noaa.var_y(obliq_corr_deg_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value, expected",
    [
    (89.3396636153339, 4126.22229222893, 0.016704231813213, 0.0430314901072543, -1.70630784072322), # geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value, expected
    (180.178861916105, 8896.83359556751, 0.0166986553093454, 0.0430315511340247, 6.83497572573191), # geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value, expected
    ]
)
def test_eq_of_time_minutes(geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value, expected):
    result = noaa.eq_of_time_minutes(geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "latitude, sun_declin_deg_value, expected",
    [
    (40, 23.4383121595139, 112.610346376993), # latitude, sun_declin_deg_value, expected
    (37.4219444444444, 0.66936449061751, 91.5613033434302), # latitude, sun_declin_deg_value, expected
    ]
)
def test_ha_sunrise_deg(latitude, sun_declin_deg_value, expected):
    result = noaa.ha_sunrise_deg(latitude, sun_declin_deg_value)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "longitude, time_zone, solar_noon_lst, expected",
    [
    (-105, -6, -1.70630784072322, 0.542851602667169), # longitude, time_zone, solar_noon_lst, expected
    (-122.079583333333, -8, 6.83497572573191, 0.501030109449723), # longitude, time_zone, solar_noon_lst, expected
    ]
)
def test_solar_noon_lst(longitude, time_zone, solar_noon_lst, expected):
    result = noaa.solar_noon_lst(longitude, time_zone, solar_noon_lst)
    almostequal(result, expected)

@pytest.mark.parametrize(
    "ha_sunrise_deg_value, solar_noon_lst_value, expected",
    [
    (112.610346376993, 0.542851602667169, 0.230045084953299), # ha_sunrise_deg_value, solar_noon_lst_value, expected
    (91.5613033434302, 0.501030109449723, 0.246693155717973), # ha_sunrise_deg_value, solar_noon_lst_value, expected
    ]
)
def test_sunrise_time_lst(ha_sunrise_deg_value, solar_noon_lst_value, expected):
    result = noaa.sunrise_time_lst(ha_sunrise_deg_value, solar_noon_lst_value)
    almostequal(result, expected)


@pytest.mark.parametrize(
    "ha_sunrise_deg_value, solar_noon_lst_value, expected",
    [
    (112.610346376993, 0.542851602667169, 0.855658120381039), # ha_sunrise_deg_value, solar_noon_lst_value, expected
    (91.5613033434302, 0.501030109449723, 0.755367063181474), # ha_sunrise_deg_value, solar_noon_lst_value, expected
    ]
)
def test_sunset_time_lst(ha_sunrise_deg_value, solar_noon_lst_value, expected):
    result = noaa.sunset_time_lst(ha_sunrise_deg_value, solar_noon_lst_value)
    almostequal(result, expected)


