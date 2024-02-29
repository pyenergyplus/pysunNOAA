# Copyright (c) 2024 Santosh Philip
# =======================================================================
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# =======================================================================
"""pytests for noaa.py"""

import pytest
import datetime
import csv
from io import StringIO
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
        (2, 4),  # a, expected
    ],
)
def test_add2(a, expected):
    result = noaa.add2(a)
    result == expected


@pytest.mark.parametrize(
    "dt, expected",
    [
        (
            datetime.datetime(2001, 10, 2, 5, 30, 35),
            datetime.datetime(2001, 10, 2),
        ),  # dt, expected
    ],
)
def test_datetime_midnight(dt, expected):
    result = noaa.datetime_midnight(dt)
    assert result == expected


@pytest.mark.parametrize(
    "dayfraction, datetime_day, expected",
    [
        (
            0.25,
            datetime.datetime(2001, 10, 5, 10, 5),
            datetime.datetime(2001, 10, 5, 6),
        ),  # dayfraction, datetime_day, expected
        (
            0.25,
            None,
            datetime.datetime(2001, 1, 1, 6),
        ),  # dayfraction, datetime_day, expected
        (
            1 / 24 * 14,
            datetime.datetime(2001, 10, 5, 10, 5),
            datetime.datetime(2001, 10, 5, 14),
        ),  # dayfraction, datetime_day, expected
    ],
)
def test_dayfraction2datetime(dayfraction, datetime_day, expected):
    result = noaa.dayfraction2datetime(dayfraction, datetime_day)
    assert result == expected


@pytest.mark.parametrize(
    "dayfraction, datetime_day, t_format, expected",
    [
        (0.25, None, None, "06:00:00"),  # dayfraction, datetime_day, t_format, expected
        (
            0.25,
            None,
            "%H|%M|%S",
            "06|00|00",
        ),  # dayfraction, datetime_day, t_format, expected
        (
            0.25,
            datetime.datetime(1900, 2, 3),
            "%H|%M|%S",
            "06|00|00",
        ),  # dayfraction, datetime_day, t_format, expected
    ],
)
def test_dayfraction2dateformat(dayfraction, datetime_day, t_format, expected):
    result = noaa.dayfraction2dateformat(dayfraction, datetime_day, t_format)
    assert result == expected


@pytest.mark.parametrize(
    "dt, expected",
    [
        (datetime.datetime(2001, 1, 1, 6), 0.25),  # dt, expected
        (datetime.datetime(2001, 1, 1, 6, 30), 0.2708333333333333),  # dt, expected
        (datetime.datetime(2001, 1, 1, 13, 30, 22), 0.5627546296296296),  # dt, expected
        (
            datetime.datetime(2001, 1, 1, 13, 30, 22, 0),
            0.5627546296296296,
        ),  # dt, expected
        (
            datetime.datetime(2001, 1, 1, 13, 30, 21, 999999),
            0.5627546296180556,
        ),  # dt, expected
    ],
)
def test_datetime2dayfraction(dt, expected):
    result = noaa.datetime2dayfraction(dt)
    assert result == expected


#     almostequal(result, expected)


@pytest.mark.parametrize(
    "dt, timezone, expected",
    [
        (
            datetime.datetime(2010, 6, 21, 0, 6),
            -6,
            2455368.75416667,
        ),  # dt, timezone, expected
        (
            datetime.datetime(2023, 9, 21, 5, 33),
            -8,
            2460209.06458333,
        ),  # dt, timezone, expected
    ],
)
def test_julianday(dt, timezone, expected):
    result = noaa.julianday(dt, timezone)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "jul_day, expected",
    [
        (2455368.75416667, 0.104688683550086),  # jul_day, expected
        (2460209.06458333, 0.237209160392435),  # jul_day, expected
    ],
)
def test_juliancentury(jul_day, expected):
    result = noaa.juliancentury(jul_day)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
        (0.104688683550086, 89.3396636153339),  # juliancentury_value, expected
        (0.237209160392435, 180.178861916105),  # juliancentury_value, expected
    ],
)
def test_geom_mean_long_sun_deg(juliancentury_value, expected):
    result = noaa.geom_mean_long_sun_deg(juliancentury_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
        (0.104688683550086, 4126.22229222893),  # juliancentury_value, expected
        (0.23720916, 8896.83359556751),  # juliancentury_value, expected
    ],
)
def test_geom_mean_anom_sun_deg(juliancentury_value, expected):
    result = noaa.geom_mean_anom_sun_deg(juliancentury_value)
    assert almostequal(result, expected, places=4)


@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
        (0.104688683550086, 0.016704231813213),  # juliancentury_value, expected
        (0.23720916, 0.0166986553093454),  # juliancentury_value, expected
    ],
)
def test_ent_earth_orbit(juliancentury_value, expected):
    result = noaa.eccent_earth_orbit(juliancentury_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, geom_mean_anom_sun_value, expected",
    [
        (
            0.104689824321243,
            4126.22229222893,
            0.446799918175887,
        ),  # juliancentury_value, geom_mean_anom_sun_value, expected
        (
            0.237209160392435,
            8896.83359556751,
            -1.85407782292307,
        ),  # juliancentury_value, geom_mean_anom_sun_value, expected
    ],
)
def test_sun_eq_of_ctr(juliancentury_value, geom_mean_anom_sun_value, expected):
    result = noaa.sun_eq_of_ctr(juliancentury_value, geom_mean_anom_sun_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected",
    [
        (
            89.3396636153339,
            0.446799918175887,
            89.7864635335097,
        ),  # geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected
        (
            180.178861916105,
            -1.85407782292307,
            178.324784093182,
        ),  # geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected
    ],
)
def test_sun_true_long_deg(geom_mean_long_sun_deg_value, sun_eq_of_ctr_value, expected):
    result = noaa.sun_true_long_deg(geom_mean_long_sun_deg_value, sun_eq_of_ctr_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected",
    [
        (
            4126.22229222893,
            0.446799918175887,
            4126.6690921471,
        ),  # geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected
        (
            8896.83359556751,
            -1.85407782292307,
            8894.97951774459,
        ),  # geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected
    ],
)
def test_sun_true_anom_deg(geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value, expected):
    result = noaa.sun_true_anom_deg(geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "eccent_earth_orbit_value, sun_true_anom_deg_value, expected",
    [
        (
            0.016704231813213,
            4126.6690921471,
            1.01624008495444,
        ),  # eccent_earth_orbit_value, sun_true_anom_deg_value, expected
        (
            0.0166986553093454,
            8894.97951774459,
            1.0040674712274,
        ),  # eccent_earth_orbit_value, sun_true_anom_deg_value, expected
    ],
)
def test_sun_rad_vector_AUs(
    eccent_earth_orbit_value, sun_true_anom_deg_value, expected
):
    result = noaa.sun_rad_vector_AUs(eccent_earth_orbit_value, sun_true_anom_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, sun_true_long_deg_value, expected",
    [
        (
            0.10468868,
            89.7864635335097,
            89.7854391814863,
        ),  # juliancentury_value, sun_true_long_deg_value, expected
        (
            0.23720916,
            178.324784093182,
            178.316980310654,
        ),  # juliancentury_value, sun_true_long_deg_value, expected
    ],
)
def test_sun_app_long_deg(juliancentury_value, sun_true_long_deg_value, expected):
    result = noaa.sun_app_long_deg(juliancentury_value, sun_true_long_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
        (0.10468868, 23.4379297208038),  # juliancentury_value, expected
        (0.23720916, 23.4362064011546),  # juliancentury_value, expected
    ],
)
def test_mean_obliq_ecliptic_deg(juliancentury_value, expected):
    result = noaa.mean_obliq_ecliptic_deg(juliancentury_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, mean_obliq_ecliptic_deg_value, expected",
    [
        (
            0.10468868,
            23.4379297208038,
            23.4384863293544,
        ),  # juliancentury_value, mean_obliq_ecliptic_deg_value, expected
        (
            0.23720916,
            23.4362064011546,
            23.4385024897594,
        ),  # juliancentury_value, mean_obliq_ecliptic_deg_value, expected
    ],
)
def test_obliq_corr_deg(juliancentury_value, mean_obliq_ecliptic_deg_value, expected):
    result = noaa.obliq_corr_deg(juliancentury_value, mean_obliq_ecliptic_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected",
    [
        (
            89.7854391814863,
            23.4384863293544,
            89.7661433042803,
        ),  # sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected
        (
            178.316980310654,
            23.4385024897594,
            178.455780149553,
        ),  # sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected
    ],
)
def test_sun_rt_ascen_deg(
    sun_app_long_deg_value, mean_obliq_ecliptic_deg_value, expected
):
    result = noaa.sun_rt_ascen_deg(
        sun_app_long_deg_value, mean_obliq_ecliptic_deg_value
    )
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "sun_app_long_deg_value, obliq_corr_deg_value, expected",
    [
        (
            89.7854391814863,
            23.4384863293544,
            23.4383121595139,
        ),  # sun_app_long_deg_value, obliq_corr_deg_value, expected
        (
            178.316980310654,
            23.4385024897594,
            0.66936449061751,
        ),  # sun_app_long_deg_value, obliq_corr_deg_value, expected
    ],
)
def test_sun_declin_deg(sun_app_long_deg_value, obliq_corr_deg_value, expected):
    result = noaa.sun_declin_deg(sun_app_long_deg_value, obliq_corr_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "obliq_corr_deg_value, expected",
    [
        (23.4384863293544, 0.0430314901072543),  # obliq_corr_deg_value, expected
        (23.4385024897594, 0.0430315511340247),  # obliq_corr_deg_value, expected
    ],
)
def test_var_y(obliq_corr_deg_value, expected):
    result = noaa.var_y(obliq_corr_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value, expected",
    [
        (
            89.3396636153339,
            4126.22229222893,
            0.016704231813213,
            0.0430314901072543,
            -1.70630784072322,
        ),  # geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value, expected
        (
            180.178861916105,
            8896.83359556751,
            0.0166986553093454,
            0.0430315511340247,
            6.83497572573191,
        ),  # geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value, expected
    ],
)
def test_eq_of_time_minutes(
    geom_mean_long_sun_deg_value,
    geom_mean_anom_sun_deg_value,
    eccent_earth_orbit_value,
    var_y_value,
    expected,
):
    result = noaa.eq_of_time_minutes(
        geom_mean_long_sun_deg_value,
        geom_mean_anom_sun_deg_value,
        eccent_earth_orbit_value,
        var_y_value,
    )
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "latitude, sun_declin_deg_value, expected",
    [
        (
            40,
            23.4383121595139,
            112.610346376993,
        ),  # latitude, sun_declin_deg_value, expected
        (
            37.4219444444444,
            0.66936449061751,
            91.5613033434302,
        ),  # latitude, sun_declin_deg_value, expected
    ],
)
def test_ha_sunrise_deg(latitude, sun_declin_deg_value, expected):
    result = noaa.ha_sunrise_deg(latitude, sun_declin_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "longitude, timezone, solar_noon_lst, expected",
    [
        (
            -105,
            -6,
            -1.70630784072322,
            0.542851602667169,
        ),  # longitude, timezone, solar_noon_lst, expected
        (
            -122.079583333333,
            -8,
            6.83497572573191,
            0.501030109449723,
        ),  # longitude, timezone, solar_noon_lst, expected
    ],
)
def test_solar_noon_lst(longitude, timezone, solar_noon_lst, expected):
    result = noaa.solar_noon_lst(longitude, timezone, solar_noon_lst)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "ha_sunrise_deg_value, solar_noon_lst_value, expected",
    [
        (
            112.610346376993,
            0.542851602667169,
            0.230045084953299,
        ),  # ha_sunrise_deg_value, solar_noon_lst_value, expected
        (
            91.5613033434302,
            0.501030109449723,
            0.246693155717973,
        ),  # ha_sunrise_deg_value, solar_noon_lst_value, expected
    ],
)
def test_sunrise_time_lst(ha_sunrise_deg_value, solar_noon_lst_value, expected):
    result = noaa.sunrise_time_lst(ha_sunrise_deg_value, solar_noon_lst_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "ha_sunrise_deg_value, solar_noon_lst_value, expected",
    [
        (
            112.610346376993,
            0.542851602667169,
            0.855658120381039,
        ),  # ha_sunrise_deg_value, solar_noon_lst_value, expected
        (
            91.5613033434302,
            0.501030109449723,
            0.755367063181474,
        ),  # ha_sunrise_deg_value, solar_noon_lst_value, expected
    ],
)
def test_sunset_time_lst(ha_sunrise_deg_value, solar_noon_lst_value, expected):
    result = noaa.sunset_time_lst(ha_sunrise_deg_value, solar_noon_lst_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "ha_sunrise_deg_value, expected",
    [
        (112.610346376993, 900.882771015944),  # ha_sunrise_deg_value, expected
        (91.5613033434302, 732.4904267474416),  # ha_sunrise_deg_value, expected
    ],
)
def test_sunlight_duration_minutes(ha_sunrise_deg_value, expected):
    result = noaa.sunlight_duration_minutes(ha_sunrise_deg_value)
    assert result == expected


@pytest.mark.parametrize(
    "thedate, eq_of_time_minutes_value, longitude, timezone, expected",
    [
        (
            datetime.datetime(2010, 6, 21, 0, 6, 0),
            -1.70630784072322,
            -105,
            -6,
            1384.29369215928,
        ),  # thedate, eq_of_time_minutes_value, longitude, timezone, expected
        (
            datetime.datetime(2023, 9, 21, 5, 33, 0),
            6.83497572573191,
            -122.079583333333,
            -8,
            331.516642392399,
        ),  # thedate, eq_of_time_minutes_value, longitude, timezone, expected
    ],
)
def test_true_solar_time_min(
    thedate, eq_of_time_minutes_value, longitude, timezone, expected
):
    result = noaa.true_solar_time_min(
        thedate, eq_of_time_minutes_value, longitude, timezone
    )
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "true_solar_time_min_value, expected",
    [
        (1384.29369215928, 166.073423039819),  # true_solar_time_min_value, expected
        (331.516642392399, -97.1208394019004),  # true_solar_time_min_value, expected
    ],
)
def test_hour_angle_deg(true_solar_time_min_value, expected):
    result = noaa.hour_angle_deg(true_solar_time_min_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "latitude, sun_declin_deg_value, hour_angle_deg_value, expected",
    [
        (
            40,
            23.4383121595139,
            166.073423039819,
            115.245718494866,
        ),  # latitude, sun_declin_deg_value, hour_angle_deg_value, expected
    ],
)
def test_solar_zenith_angle_deg(
    latitude, sun_declin_deg_value, hour_angle_deg_value, expected
):
    result = noaa.solar_zenith_angle_deg(
        latitude, sun_declin_deg_value, hour_angle_deg_value
    )
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "solar_zenith_angle_deg_value, expected",
    [
        (115.245718494866, -25.245718494866),  # solar_zenith_angle_deg_value, expected
        (95.2408647936783, -5.24086479367834),  # solar_zenith_angle_deg_value, expected
    ],
)
def test_solar_elevation_angle_deg(solar_zenith_angle_deg_value, expected):
    result = noaa.solar_elevation_angle_deg(solar_zenith_angle_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "solar_elevation_angle_deg_value, expected",
    [
        (
            -25.245718494866,
            0.0122365205193627,
        ),  # solar_elevation_angle_deg_value, expected
        (
            -5.24086479367834,
            0.0629045265211758,
        ),  # solar_elevation_angle_deg_value, expected
    ],
)
def test_approx_atmospheric_refraction_deg(solar_elevation_angle_deg_value, expected):
    result = noaa.approx_atmospheric_refraction_deg(solar_elevation_angle_deg_value)
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "solar_elevation_angle_deg_value, approx_atmospheric_refraction_deg_value, expected",
    [
        (
            -25.245718494866,
            0.0122365205193627,
            -25.2334819743467,
        ),  # solar_elevation_angle_deg_value, approx_atmospheric_refraction_deg_value, expected
        (
            -5.24086479367834,
            0.0629045265211758,
            -5.17796026715717,
        ),  # solar_elevation_angle_deg_value, approx_atmospheric_refraction_deg_value, expected
    ],
)
def test_solar_elevation_corrected_for_atm_refraction_deg(
    solar_elevation_angle_deg_value, approx_atmospheric_refraction_deg_value, expected
):
    result = noaa.solar_elevation_corrected_for_atm_refraction_deg(
        solar_elevation_angle_deg_value, approx_atmospheric_refraction_deg_value
    )
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "latitude, hour_angle_deg, solar_zenith_angle_deg_value, sun_declin_deg_value, expected",
    [
        (
            40,
            166.073423039819,
            115.245718494866,
            23.4383121595139,
            345.86910228316,
        ),  # latitude, hour_angle_deg, solar_zenith_angle_deg_value, sun_declin_deg_value, expected
        (
            37.4219444444444,
            -97.1208394019004,
            95.2408647936783,
            0.66936449061751,
            85.1264242410581,
        ),  # latitude, hour_angle_deg, solar_zenith_angle_deg_value, sun_declin_deg_value, expected
        (
            40,
            -178.928841894617,
            116.553762119181,
            23.4383706192869,
            1.09867118388445,
        ),  # latitude, hour_angle_deg, solar_zenith_angle_deg_value, sun_declin_deg_value, expected
    ],
)
def test_solar_azimuth_angle_deg_cw_from_n(
    latitude,
    hour_angle_deg,
    solar_zenith_angle_deg_value,
    sun_declin_deg_value,
    expected,
):
    result = noaa.solar_azimuth_angle_deg_cw_from_n(
        latitude, hour_angle_deg, solar_zenith_angle_deg_value, sun_declin_deg_value
    )
    assert almostequal(result, expected)


@pytest.mark.parametrize(
    "start, stop, minutes_step, expected",
    [
        (
            datetime.datetime(2024, 2, 3, 1),
            datetime.datetime(2024, 2, 3, 3),
            60,
            [datetime.datetime(2024, 2, 3, 1), datetime.datetime(2024, 2, 3, 2)],
        ),  # start, stop, minutes_step, expected
        (
            datetime.datetime(2024, 2, 3, 1),
            datetime.datetime(2024, 2, 3, 3),
            30,
            [
                datetime.datetime(2024, 2, 3, 1, 0),
                datetime.datetime(2024, 2, 3, 1, 30),
                datetime.datetime(2024, 2, 3, 2),
                datetime.datetime(2024, 2, 3, 2, 30),
            ],
        ),  # start, stop, minutes_step, expected
    ],
)
def test_datetimerange(start, stop, minutes_step, expected):
    result = noaa.datetimerange(start, stop, minutes_step)
    assert list(result) == expected


@pytest.mark.parametrize(
    "latitude, longitude, timezone, thedate, atm_corr, expected",
    [
        (
            40,
            -105,
            -6,
            datetime.datetime(2010, 6, 21, 0, 6),
            True,
            (-25.2334819743467, 345.86910228316),
        ),  # latitude, longitude, timezone, thedate, atm_corr, expected
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            datetime.datetime(2023, 9, 21, 5, 33),
            True,
            (-5.17796026715717, 85.1264242410581),
        ),  # latitude, longitude, timezone, thedate, atm_corr, expected
        (
            40,
            -105,
            -6,
            datetime.datetime(2010, 6, 21, 0, 6),
            False,
            (-25.245718494866, 345.86910228316),
        ),  # latitude, longitude, timezone, thedate, atm_corr, expected
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            datetime.datetime(2023, 9, 21, 5, 33),
            False,
            (-5.24086479367834, 85.1264242410581),
        ),  # latitude, longitude, timezone, thedate, atm_corr, expected
    ],
)
def test_sunposition(latitude, longitude, timezone, thedate, atm_corr, expected):
    result_alt, result_azm = noaa.sunposition(
        latitude, longitude, timezone, thedate, atm_corr
    )
    expected_alt, expected_azm = expected
    assert almostequal(result_alt, expected_alt)
    assert almostequal(result_azm, expected_azm)


@pytest.mark.parametrize(
    "latitude, longitude, timezone, thedates, atm_corr, expected",
    [
        (
            40,
            -105,
            -6,
            noaa.datetimerange(
                datetime.datetime(2010, 6, 21, 0, 6),
                datetime.datetime(2010, 6, 21, 0, 24),
                6,
            ),
            True,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-25.2334819743467,   345.86910228316
-25.499566275192,   347.363394492955
-25.7363046548659,  348.866858015593
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
        (
            40,
            -105,
            -6,
            noaa.datetimerange(
                datetime.datetime(2010, 6, 21, 0, 6),
                datetime.datetime(2010, 6, 22, 0, 0),
                6,
            ),
            True,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-25.2334819743467,345.86910228316
-25.499566275192,347.363394492955
-25.7363046548659,348.866858015593
-25.9433646052138,350.378512732807
-26.12045127645,351.897331655263
-26.267309472218,353.422246027742
-26.3837254112775,354.952150988432
-26.4695282284935,356.485911720329
-26.5245911910409,358.022370018731
-26.5488326100602,359.560351189686
-26.5422164325894,1.09867118388445
-26.504752503903,2.63614386580969
-26.4364964958038,4.17158831262935
-26.337549502092,5.70383603820096
-26.2080573080211,7.23173803789319
-26.0482093459121,8.75417155641839
-25.858237354152,10.2700464868082
-25.6384137612785,11.7783113192214
-25.3890498206689,13.2779585697837
-25.1104935245949,14.7680296316671
-24.8031273285503,16.2476190058521
-24.4673657184806,17.7158778816055
-24.1036526539533,19.172017052416
-23.712458920456,20.6153091650712
-23.2942794227916,22.0450903137511
-22.8496304502974,23.4607610007815
-22.379046942024,24.8617864971123
-21.8830797776677,26.2476966422166
-21.3622931163886,27.6180851311283
-20.8172618024823,28.9726083395377
-20.2485688523667,30.3109837424229
-19.6568030333838,31.6329879818931
-19.0425565397608,32.9384546408456
-18.40642276554,34.2272717779075
-17.7489941682159,35.4993792762134
-17.0708602084128,36.754766056848
-16.3726053414969,37.9934672027996
-15.6548070226422,39.2155610366279
-14.9180336680278,40.4211661893665
-14.1628424848911,41.6104386951088
-13.3897770384191,42.7835691399645
-12.5993643491368,43.9407798910859
-11.7921111919922,45.0823224260528
-10.9684990531569,46.2084747803346
-10.1289768134131,47.3195391257453
-9.27394949194995,48.4158394908254
-8.40375992283372,49.4977196301484
-7.51865714317526,50.5655410477247
-6.61873824277419,51.6196811774994
-5.70383297563267,52.6605317214901
-4.77325201262117,53.6884971456187
-3.82516424927518,54.7039933309497
-2.85475750001635,55.7074463782421
-1.84707024577665,56.6992915619059
-0.729664707308368,57.6799724300869
0.422420619818739,58.6499400462365
1.28798788313787,59.6096523684939
2.20175934394734,60.5595737622039
3.14992917410838,61.5001746421249
4.12273265477486,62.4319312401593
5.11490902618878,63.3553254958562
6.12407315254798,64.2708450665604
7.14545807207465,65.1789834552292
8.17795619562933,66.0802402546079
9.2203755372119,66.9751215066672
10.2717779509596,67.8641401778856
11.331407533357,68.7478167509043
12.3986386454706,69.626679935014
13.4729389808988,70.5012674980387
14.5538438427539,71.3721272242726
15.6409382680225,72.2398180034306
16.733844491998,73.1049110578651
17.832213017574,73.9679913158527
18.9357161255304,74.8296589413109
20.0440430494116,75.690531031177
21.1568962967774,76.5512434945695
22.2739887660265,77.4124531292592
23.3950414192227,78.2748399139376
24.519781344406,79.1391095375199
25.6479400888559,80.0059961893104
26.7792521785162,80.8762656381351
27.9134537596735,81.750718631559
29.0502813151844,82.6301946516568
30.1894704164337,83.5155760678931
31.330754480179,84.4077927342678
32.4738635025236,85.307827083391
33.6185227460565,86.2167197783725
34.7644513561503,87.13557599074
35.911360883776,88.0655723828968
37.0589536901349,89.0079648832434
38.2069212080115,89.9640973549392
39.3549420312285,90.9354112718009
40.5026798010365,91.9234565302718
41.6497808541935,92.9299035429489
42.7958715917881,93.956556776723
43.940555522909,95.0053699191154
45.0834099288029,96.0784628761842
46.2239820858474,97.1781408279001
47.3617849743249,98.3069155869589
48.4962923894074,99.4675295274201
49.6269333557466,100.662982363516
50.7530857324,101.896561067381
51.874068875355,103.171873207295
52.989135205565,104.492883962128
54.0974605063083,105.86395700678
55.1981327501602,107.289899356044
56.2901392290927,108.776010072348
57.372351736888,110.328132458083
58.4435095316433,111.952708918206
59.502199792415,113.656837032353
60.5468352878091,115.44832444001
61.5756290030677,117.335738807647
62.5865655474712,119.328447290672
63.577369305537,121.43663737
64.5454695425593,123.67130758917
65.4879630689664,126.044212421207
66.4015756715996,128.567740264205
67.2826243962001,131.254697646958
68.1269839840596,134.117966859036
68.9300623623145,137.169999908703
69.6867920345177,140.422111632585
70.3916463379469,143.883543012358
71.0386914177172,147.560287671097
71.6216856704344,151.453715632978
72.1342372366917,155.559091611348
72.5700255902533,159.864165906024
72.9230843888913,164.348097266033
73.1881296413684,168.981016568875
73.360902029692,173.724516981045
73.4384793439627,178.533230037882
73.4195101233167,183.3574244066
73.3043270973898,188.146304468253
73.094918937806,192.851486254074
72.7947657532213,197.430075203458
72.4085688801049,201.846887993571
71.9419209175668,206.075596047525
71.4009643050083,210.09882372923
70.792078068548,213.907423165796
70.1216179125423,217.499231602807
69.3957200365671,220.877607092995
68.6201674803997,224.049971675359
67.8003106931593,227.026507070503
66.9410309572938,229.819072793473
66.046735089679,232.440362057604
65.1213712407828,234.903277840968
64.1684576585614,237.220495626809
63.1911183687445,239.40417494219
62.192121544398,241.465783962096
61.1739177836943,243.416006615861
60.1386765929613,245.264707646808
59.0883201322793,247.020936780467
58.024553795248,248.692958031527
56.9488935242359,250.288294098692
55.8626899630572,251.813778811829
54.7671496619889,253.275612843321
53.6633536033639,254.679419532228
52.5522733346428,256.030298831681
51.4347849901469,257.332878203311
50.3116814667124,258.591359835343
49.1836829941277,259.809563932717
48.0514463168195,260.990968065823
46.9155726766287,262.138742715166
45.7766147636058,263.255783234857
44.6350827785863,264.34473850451
43.4914497328153,265.408036555417
42.3461560914345,266.447907458186
41.1996138536245,267.466403747037
40.0522101485771,268.465418639567
38.9043104153421,269.446702290497
37.7562612257823,270.411876295845
36.6083928008061,271.362446643728
35.4610212644707,272.299815286409
34.3144506737356,273.225290490338
33.1689748581921,274.140096102247
32.0248790991763,275.045379854608
30.8824416759381,275.942220818357
29.7419353032462,276.831636099089
28.6036284846735,277.714586860496
27.4677868041731,278.591983749817
26.3346741802472,279.464691790065
25.20455410755,280.333534797028
24.0776909149794,281.199299371095
22.9543510738543,282.062738508498
21.8348045977068,282.924574871073
20.7193265876629,283.78550374836
19.6081989938281,284.646195742523
18.5017126899658,285.507299201812
17.4001699957988,286.36944242603
16.303887839414,287.233235663445
15.2132018370303,288.099272917031
14.1284716989189,288.968133574496
13.0500885681026,289.840383875501
11.9784852025525,290.716578226499
10.9141503648378,291.597260372981
9.85764943591629,292.482964436247
8.80965410307731,293.374215821478
7.77098475176772,294.271532001601
6.74266941805119,295.175423180854
5.72602704943685,296.086392840823
4.72277345735459,297.004938170129
3.73786333149665,297.931550378917
2.77382780596289,298.866714897418
1.83775283902547,299.810911458071
0.94104893148275,300.764614058952
0.0989819972925181,301.72829080667
-1.19505705429213,302.70240363522
-2.24979435294097,303.687407897955
-3.23963665336637,304.683751828306
-4.20037140373879,305.691875865777
-5.14127074415214,306.712211842429
-6.06559172435652,307.74518202626
-6.97459755353511,308.791198016969
-7.86872827057114,309.850659490654
-8.74802925470869,310.923952790492
-9.61233408706253,312.011449360636
-10.4613518010267,313.113504022617
-11.2947122634518,314.230453093694
-12.1119915018131,315.362612349445
-12.9127267305376,316.510274833584
-13.6964257887734,317.673708521563
-14.4625734153801,318.853153845854
-15.2106356797549,320.048821095131
-15.9400633182744,321.260887701559
-16.6502944211346,322.489495435436
-17.3407567420204,323.734747529018
-18.0108698035239,324.996705756898
-18.6600469100323,326.275387503495
-19.2876971421161,327.570762853373
-19.8932273815996,328.882751744546
-20.4760443993032,330.211221228331
-21.0355570258597,331.555982884498
-21.5711784164066,332.91679044237
-22.08232841325,334.293337662685
-22.5684360041053,335.685256535309
-23.0289418687351,337.09211585005
-23.4633010017024,338.513420195657
-23.8709853950992,339.948609441546
-24.251486760873,341.397058751514
-24.6043192692371,342.858079174853
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            noaa.datetimerange(
                datetime.datetime(2023, 9, 21, 5, 33),
                datetime.datetime(2023, 9, 21, 5, 36),
                1,
            ),
            True,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-5.17796026715717,	85.1264242410581
-4.9777465279639,	85.2800907071635
-4.77728643338201,	85.4336534862891
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            noaa.datetimerange(
                datetime.datetime(2023, 9, 21, 5, 33),
                datetime.datetime(2023, 9, 21, 17, 50),
                1,
            ),
            True,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-5.17796026715717,85.1264242410581
-4.9777465279639,85.2800907071635
-4.77728643338201,85.4336534862891
-4.57655553232449,85.5871163110677
-4.37552475482894,85.7404829080009
-4.17415933634022,85.8937569977111
-3.97241742632934,86.0469422951765
-3.77024826766484,86.2000425099902
-3.56758978385218,86.3530613465979
-3.36436533662599,86.5060025045469
-3.16047930084704,86.6588696787374
-2.95581092092056,86.811666559827
-2.75020561574972,86.9643968338112
-2.54346240570298,87.1170641832801
-2.33531527913683,87.269672286986
-2.12540479505561,87.4222248202637
-1.91323338068746,87.5747254552722
-1.69809224613516,87.7271778612431
-1.47893640328349,87.8795857047292
-1.25415902707575,88.0319526498428
-1.02115591632549,88.1842823585149
-0.775410451209581,88.3365784907289
-0.508344752527223,88.4888447049431
-0.201433596691516,88.6410846576603
0.073060867791875,88.7933020046859
0.238153224779796,88.9455004007024
0.40576450283286,89.0976834996826
0.575720395334959,89.2498549551361
0.747853832127219,89.4020184203577
0.922004993983489,89.554177548673
1.09802132603701,89.7063359936884
1.27575755016229,89.8584974095368
1.45507567631445,90.0106654511214
1.63584501274928,90.1628437745391
1.81794217555858,90.3150360366499
2.00125109645983,90.4672458963357
2.18566303024569,90.6194770140759
2.37107656084491,90.7717330523639
2.55739760641363,90.9240176759545
2.74453942338497,91.0763345521179
2.93242260948517,91.2286873508808
3.12097510570527,91.3810797452811
3.3101321972361,91.5335154116161
3.49983651336422,91.6859980296911
3.6900380262499,91.8385312832439
3.88069404904322,91.9911188595091
4.07176923220736,92.1437644504934
4.26323555954882,92.2964717525431
4.45507234282936,92.4492444667673
4.64726621540741,92.6020862992909
4.83981112483634,92.7550009615025
5.03270832441026,92.9079921703114
5.22644404160491,93.0610636483957
5.41997447655297,93.2142191244571
5.61370207326123,93.3674623334768
5.80760970560932,93.520797016964
6.00168214378279,93.674226923383
6.19590555997516,93.8277558077283
6.3902672180603,93.9813874327975
6.58475527470577,94.1351255687679
6.77935864673919,94.2889739936201
6.97406691891295,94.4429364933956
7.16887027624235,94.5970168624524
7.36375945148112,94.7512189037234
7.55872568209653,94.9055464289722
7.75376067338139,95.0600032590499
7.94885656570879,95.2145932241545
8.14400590468132,95.3693201642585
8.33920161394417,95.5241879286906
8.53443696910725,95.6792003774104
8.72970557406995,95.8343613805915
8.92500133845008,95.9896748190499
9.12031845647667,96.1451445845071
9.31565138719961,96.3007745798498
9.51099483595307,96.4565687193895
9.70634373701371,96.6125309291273
9.90169323740141,96.7686651470145
10.0970386817625,96.9249753232176
10.292375598203,97.0814654205511
10.4876996854852,97.238139414055
10.6830068003479,97.39500129229
10.8782929464725,97.5520550569126
11.0735542638535,97.709304723116
11.2687870189982,97.8667543198912
11.4639875958217,98.0244078902944
11.6591524871872,98.1822694917151
11.8542782870524,98.3403431961381
12.0493616831677,98.4986330904156
12.2443994502958,98.6571432765296
12.4393884438265,98.8158778720334
12.6343255942309,98.9748410096336
12.8292079011333,99.1340368384852
13.0240324285501,99.2934695237774
13.2187963000844,99.4531432471715
13.413496694522,99.6130622070692
13.6081308417228,99.773230618883
13.8026960187904,99.9336527153052
13.9971895464927,100.094332746579
14.1916087859197,100.255274980767
14.3859511353586,100.416483704018
14.5802140273667,100.577963220844
14.7743949259523,100.739717854557
14.9684913243262,100.90175194685
15.1625007420117,101.064069859106
15.3564207229018,101.226675971972
15.550248833052,101.389574685807
15.7439826586792,101.552770420949
15.9376198042765,101.716267617989
16.1311578908387,101.880070738033
16.3245945541845,102.044184262978
16.5179274433743,102.20861269578
16.7111542192109,102.373360560725
16.9042725527447,102.538432403863
17.0972801242559,102.703832792593
17.2901746214911,102.869566316964
17.4829537387816,103.03563758925
17.6756151758109,103.202051244396
17.8681566365232,103.368811940276
18.0605758280786,103.535924357962
18.2528704598614,103.70339320199
18.4450382425295,103.871223200622
18.6370768871062,104.039419106109
18.828984104113,104.207985694954
19.0207576026531,104.376927768348
19.2123950899443,104.54625015173
19.403894270056,104.715957696092
19.5952528434979,104.886055277546
19.7864685064319,105.056547797743
19.9775389499842,105.227440184134
20.1684618595841,105.398737390225
20.3592349143261,105.570444395823
20.5498557863481,105.742566207291
20.740322140237,105.91510785779
20.9306316324444,106.08807440753
21.1207819106386,106.261470944187
21.3107706134957,106.43530258244
21.5005953696564,106.609574465268
21.6902537975441,106.784291763482
21.8797435047762,106.959459676133
22.0690620876643,107.135083430747
22.2582071307321,107.311168283552
22.4471762062418,107.487719519703
22.6359668737288,107.664742453503
22.8245766795467,107.842242428625
23.0130031564193,108.020224818326
23.2012438230023,108.19869502566
23.3892961833639,108.377658483863
23.5771577269089,108.557120655844
23.7648259274347,108.737087035456
23.9522982430689,108.917563146977
24.1395721157702,109.098554545485
24.3266449709319,109.280066817032
24.5135142169769,109.462105578841
24.7001772449678,109.644676479469
24.8866314282155,109.827785198986
25.0728741218898,110.011437449141
25.2589026626423,110.195638973513
25.4447143681294,110.380395547854
25.6303065369982,110.565712979513
25.8156764479734,110.751597108653
26.0008213598385,110.938053807673
26.1857385109816,111.125088981506
26.3704251190241,111.312708567744
26.5548783804522,111.50091853675
26.7390954702551,111.689724891757
26.9230735415573,111.879133668973
27.1068097252591,112.069150937658
27.2903011296733,112.259782800209
27.4735448400714,112.451035392409
27.656537918695,112.642914882761
27.8392774038424,112.835427473627
28.0217603098772,113.028579400543
28.2039836267825,113.222376932426
28.3859443197985,113.416826371598
28.5676393290683,113.611934053792
28.7490655692815,113.80770634814
28.9302199293151,114.004149657172
29.1110992718814,114.201270416768
29.2917004331672,114.399075096134
29.4720202223848,114.597570197917
29.6520554217972,114.796762257414
29.8318027857906,114.996657843578
30.0112590408987,115.197263558195
30.1904208853522,115.398586035948
30.3692849887205,115.600631944299
30.5478479915596,115.803407983334
30.7261065050535,116.006920885607
30.9040571106589,116.211177415959
31.0816963597482,116.416184371327
31.2590207732537,116.621948580527
31.4360268413148,116.828476904017
31.612711022818,117.03577623384
31.7890697454395,117.243853492602
31.9650994046965,117.452715634298
32.140796363987,117.662369643251
32.3161569541352,117.872822533966
32.4911774730376,118.084081350772
32.6658541853068,118.296153167442
32.8401833219187,118.509045086788
33.0141610798599,118.722764240233
33.1877836217734,118.937317787357
33.3610470756075,119.152712915416
33.5339475341609,119.368956839031
33.7064810551421,119.5860567989
33.8786436602071,119.804020062363
34.0504313350197,120.022853922063
34.2218400288023,120.242565695517
34.3928656539902,120.463162724467
34.5635040858865,120.684652374203
34.7337511623224,120.907042032846
34.9036026833135,121.130339110613
35.0730544107241,121.354551039032
35.242102067928,121.579685270139
35.4107413393711,121.805749275813
35.5789678706606,122.03275054615
35.7467772676034,122.260696589666
35.9141650963031,122.48959493159
36.0811268827272,122.719453113065
36.2476581123933,122.950278690104
36.413754230049,123.182079232521
36.5794106393605,123.414862322817
36.7446227026048,123.648635555018
36.9093857403619,123.883406533482
37.0736950312199,124.119182871645
37.2375458113676,124.355972190927
37.4009332747414,124.593782118639
37.5638525720866,124.832620287734
37.7262988111119,125.072494334621
37.8882670561098,125.313411897874
38.0497523276881,125.555380616704
38.2107496025072,125.798408129381
38.3712538130292,126.042502071596
38.5312598472676,126.287670074786
38.6907625485506,126.533919764385
38.849756715288,126.781258758041
39.0082371007465,127.029694663761
39.1661984127231,127.279235078194
39.3236353137935,127.529887583917
39.4805424204313,127.781659748543
39.6369143032783,128.034559121883
39.7927454868527,128.288593233995
39.9480304493816,128.543769592979
40.1027636226489,128.800095682712
40.2569393918478,129.057578960518
40.4105520954522,129.316226854772
40.5635960250955,129.576046762442
40.7160654254632,129.83704604657
40.8679544940832,130.099232033858
41.0192573817182,130.362612011264
41.1699681915918,130.627193224399
41.3200809798112,130.892982873976
41.469589755211,131.159988113142
41.6184884793397,131.428216044524
41.7667710664538,131.697673717231
41.9144313835328,131.96836812377
42.0614632503128,132.240306196894
42.2078604393331,132.513494806378
42.3536166760107,132.787940755714
42.4987256386024,133.063650778928
42.6431809588062,133.340631536384
42.7869762211534,133.618889612383
42.930104963648,133.898431510823
43.0725606778195,134.179263651707
43.2143368089157,134.4613923674
43.35542675612,134.744823898806
43.4958238727935,135.029564391474
43.635521466742,135.315619891619
43.7745128005058,135.60299634208
43.9127910916775,135.891699578198
44.050349513115,136.181735323807
44.1871811938276,136.473109186216
44.3232792186028,136.76582665299
44.4586366289471,137.059893086785
44.5932464234129,137.355313721049
44.7271015580844,137.652093655463
44.8601949470922,137.950237851321
44.9925194631641,138.249751126821
45.1240679382,138.550638152316
45.2548331638878,138.852903445473
45.3848078923464,139.156551366383
45.5139848368035,139.461586112608
45.6423566721787,139.768011714336
45.7699160363628,140.075832028583
45.896655530207,140.385050735145
46.0225677188711,140.695671330685
46.1476451325524,141.007697123671
46.2718802673827,141.321131229081
46.3952655863608,141.635976563065
46.5177935203279,141.952235837563
46.6394564689783,142.269911554875
46.7602468019146,142.589006002202
46.8801568597424,142.909521246144
46.9991789550645,143.231459127347
47.1173053742162,143.554821254235
47.2345283776476,143.8796089985
47.3508402017421,144.205823488785
47.4662330599863,144.533465605245
47.5806991443102,144.862535973925
47.6942306264872,145.193034961125
47.806819659564,145.524962667767
47.9184583793457,145.858318923762
48.0291389059193,146.193103282393
48.1388533452221,146.52931501471
48.2475937905156,146.866953104113
48.3553523246234,147.206016240098
48.4621210207671,147.54650281378
48.5678919448999,147.888410911696
48.6726571573562,148.23173831054
48.7764087146925,148.576482471774
48.8791386715785,148.922640536281
48.9808390827246,149.270209319104
49.0815020048637,149.619185304239
49.1811194987702,149.96956463952
49.279683631328,150.32134313158
49.377186477487,150.674516241084
49.4736201230231,151.029079077214
49.5689766658274,151.38502639395
49.6632482187539,151.74235258478
49.7564269117393,152.101051678389
49.8485048941351,152.461117334296
49.939474337065,152.822542838647
50.0293274358244,153.185321100147
50.1180564123285,153.549444646156
50.2056535175782,153.914905618951
50.2921110341849,154.281695772156
50.3774212789147,154.649806467365
50.4615766051165,155.019228671102
50.5445694059642,155.389952951208
50.6263921161656,155.761969474997
50.7070372152651,156.135268006058
50.7864972301985,156.509837902074
50.8647647380181,156.88566811271
50.9418323686582,157.262747177744
51.0176928077126,157.64106322545
51.0923387992386,158.020603971231
51.1657631485852,158.401356716518
51.2379587252256,158.78330834795
51.3089184654596,159.166445336959
51.3786353759248,159.55075373894
51.4471025355134,159.936219194138
51.5143130989063,160.322826927409
51.5802602993113,160.710561748987
51.6449374513587,161.099408055444
51.7083379540172,161.489349830938
51.7704552934851,161.880370648813
51.8312830460987,162.272453673501
51.8908148812241,162.665581662767
51.9490445641423,163.059736970296
52.0059659587615,163.454901548737
52.0615730311402,163.851056952441
52.1158598513377,164.248184341861
52.168820596903,164.646264486973
52.2204495555096,165.045277771723
52.2707411277378,165.445204198671
52.3196898298224,165.846023394007
52.3672902963696,166.247714612904
52.4135372830473,166.650256745229
52.4584256692277,167.053628321605
52.5019504606002,167.457807519817
52.5441067915643,167.862772171688
52.5848899284343,168.268499769706
52.6242952708864,168.67496747517
52.6623183550579,169.082152125504
52.6989548557501,169.490030242472
52.7342005887326,169.898578040625
52.768051512994,170.307771436058
52.8005037329291,170.717586055479
52.8315535004586,171.1279972456
52.8611972170846,171.538980082815
52.8894314358748,171.950509383175
52.9162528633716,172.362559712654
52.9416583612496,172.775105397781
52.9656449487794,173.188120536044
52.988209803449,173.601579007542
53.0093502632621,174.015454485889
53.0290638280714,174.429720449842
53.0473481610051,174.844350195061
53.0642010898048,175.259316846067
53.0796206080696,175.674593368401
53.0936048764125,176.090152580968
53.1061522235235,176.505967168545
53.1172611471314,176.92200969445
53.1269303147049,177.338252613427
53.1351585649375,177.754668284261
53.1419449073516,178.171228983308
53.1472885235922,178.587906917313
53.1511887677229,179.004674236717
53.153645166608,179.421503048947
53.1546574201829,179.83836543176
53.154225401634,180.255233446629
53.1523491574696,180.672079152112
53.1490289074891,181.088874617276
53.1442650446578,181.505591935075
53.1380581346895,181.922203235776
53.130408916443,182.338680700019
53.1213183003956,182.754996572449
53.1107873688378,183.171123174648
53.09881737506,183.587032918283
53.0854097426186,184.002698318095
53.0705660645084,184.418092004762
53.0542881022353,184.833186737626
53.0365777847965,185.247955417276
53.017437207568,185.662371097962
52.9968686310958,186.076406999834
52.974874479616,186.490036521032
52.9514573404009,186.903233249366
52.9266199611876,187.315970974197
52.9003652493518,187.728223697671
52.8726962700839,188.13996564592
52.8436162446643,188.551171279979
52.8131285486638,188.961815306435
52.7812367100676,189.371872687806
52.7479444073215,189.781318652648
52.7132554673105,190.190128705355
52.677173863264,190.598278635683
52.6397037125993,191.00574452795
52.6008492745161,191.412502769958
52.56061494845,191.818530061484
52.5190052706242,192.223803422658
52.476024912388,192.628300201799
52.431678677588,193.031998083025
52.3859715000656,193.434875093496
52.3389084411097,193.836909610322
52.2904946868707,194.238080367123
52.2407355457246,194.638366460235
52.189636445608,195.037747354574
52.1372029313124,195.436202889147
52.0834406615587,195.833713282208
52.0283554069817,196.230259136064
51.9719530462125,196.625821441535
51.9142395638166,197.02038158206
51.8552210472652,197.413921337448
51.7949036840823,197.806422887292
51.7332937589764,198.197868814039
51.6703976509562,198.58824210571
51.6062218304409,198.977526158294
51.5407728563642,199.365704777799
51.4740573732689,199.75276218198
51.4060821082202,200.138683001724
51.3368538686397,200.523452282193
51.2663795382994,200.907055483503
51.1946660751667,201.289478481242
51.1217205083304,201.670707566615
51.0475499351315,202.050729446305
50.9721615182938,202.429531242047
50.8955624830816,202.807100489921
50.8177601144655,203.183425139365
50.7387617543122,203.558493551931
50.6585747985879,203.932294499769
50.5772066944134,204.304817163833
50.4946649380512,204.676051132005
50.4109570710832,205.045986396659
50.3260906784584,205.414613352317
50.2400733856443,205.781922792926
50.152912856002,206.147905908956
50.0646167881823,206.512554284293
49.9751929135665,206.875859892939
49.8846489937344,207.237815095525
49.7929928179687,207.598412635644
49.7002322008022,207.957645636015
49.6063749795979,208.315507594492
49.5114290119832,208.671992379857
49.4154021742506,209.027094227724
49.3183023579487,209.380807735819
49.2201374683686,209.733127859612
49.1209154221403,210.084049907586
49.0206441450576,210.433569536448
48.9193315699579,210.78168274623
48.8169856346236,211.128385875291
48.7136142797532,211.473675595238
48.6092254469576,211.817548905758
48.5038270768107,212.160003129376
48.3974271067582,212.501035906084
48.2900334699851,212.840645188217
48.1816540925063,213.178829234663
48.072296892128,213.515586605639
47.9619697765322,213.850916157109
47.8506806416008,214.184817035246
47.7384373697815,214.517288670854
47.6252478284953,214.848330773767
47.5111198685932,215.177943327238
47.3960613228541,215.506126582311
47.2800800045301,215.832881052184
47.163183705758,216.158207506513
47.0453801969054,216.482106966057
46.9266772241737,216.804580696639
46.8070825090343,217.125630203817
46.6866037468088,217.445257227222
46.5652486054788,217.763463734995
46.4430247245262,218.080251918239
46.3199397138267,218.39562418551
46.1960011525759,218.709583157336
46.0712165882567,219.022131660774
45.9455935356532,219.333272724009
45.8191394757161,219.643009570913
45.6918618553621,219.951345616053
45.5637680855357,220.258284458947
45.434865541077,220.563829879171
45.3051615597479,220.867985831117
45.1746634414655,221.170756438896
45.0433784475714,221.47214599129
44.9113138001415,221.772158936769
44.7784766813211,222.07079987857
44.6448742327028,222.368073569839
44.5105135547314,222.663984908839
44.3754017061397,222.958538934224
44.2395457032491,223.251740820293
44.1029525201647,223.543595872759
43.9656290872592,223.834109523697
43.8275822914348,224.123287327454
43.6888189755354,224.411134956186
43.5493459379625,224.697658195558
43.4091699323243,224.982862940513
43.268297667101,225.266755191123
43.126735805351,225.549341048508
42.9844909644242,225.83062671083
42.8415697157146,226.110618469364
42.6979785842617,226.389322704549
42.5537240492287,226.666745882591
42.408812542693,226.942894551184
42.2632504501691,227.217775336263
42.1170441103043,227.491394938356
41.9701998147543,227.763760129103
41.8227238080911,228.034877747848
41.6746222877232,228.304754698314
41.5259014038344,228.573397945338
41.3765672593477,228.840814511693
41.2266259099008,229.107011474971
41.0760833636699,229.371995964443
40.9249455820619,229.635775158499
40.7732184787222,229.89835628114
40.6209079202595,230.159746599556
40.4680197261327,230.419953421269
40.3145596687222,230.67898409144
40.1605334734215,230.936845990254
40.0059468187323,231.19354653036
39.8508053363829,231.449093154389
39.6951146114522,231.703493332527
39.538880182509,231.956754560164
39.3821075415927,232.208884355488
39.2248021350461,232.459890257683
39.0669693626817,232.70977982412
38.9086145786358,232.95856062868
38.7497430913912,233.206240259594
38.5903601639804,233.452826317458
38.4304710141944,233.698326413301
38.2700808148035,233.942748166712
38.109194693787,234.186099204022
37.9478177345673,234.428387156548
37.7859549762516,234.669619658874
37.6236114138868,234.90980434721
37.4607919985509,235.148948857669
37.2975016382731,235.38706082516
37.1337451973224,235.624147881232
36.9695274971345,235.860217653052
36.8048533164406,236.095277761905
36.6397273915439,236.329335821828
36.4741544166196,236.562399438305
36.3081390440114,236.794476207002
36.1416858845278,237.025573712548
35.9747995077596,237.25569952736
35.8074844423795,237.484861210509
35.6397451763019,237.713066306513
35.4715861576452,237.94032234474
35.3030117940813,238.166636837719
35.1340264538107,238.392017280619
34.9646344657264,238.616471150201
34.7948401197422,238.840005903921
34.6246476671299,239.06262897907
34.4540613208501,239.284347791945
34.2830852558931,239.505169737061
34.1117236096172,239.725102186393
33.9399804820882,239.944152488647
33.7678599362668,240.16232796846
33.5953659989887,240.379635926189
33.4225026603532,240.596083636598
33.2492738747113,240.811678348713
33.0756835608539,241.026427285135
32.9017356023593,241.240337641493
32.7274338479484,241.453416585932
32.5527821118311,241.665671258619
32.3777841740638,241.877108771278
32.2024437808995,242.087736206755
32.0267646451403,242.2975606186
31.8507504463379,242.506589030559
31.6744048317747,242.714828436676
31.497731415876,242.922285800246
31.3207337811926,243.128968053963
31.1434154786009,243.334882099495
30.9657800276586,243.540034807208
30.7878309169593,243.744433015906
30.6095716044893,243.948083532586
30.4310055179838,244.150993132221
30.2521360552781,244.353168557549
30.0729665846741,244.554616518898
29.8935004452845,244.755343694005
29.7137409472421,244.955356727759
29.5336913726729,245.154662232526
29.35335497512,245.35326678733
29.1727349805241,245.551176938219
28.99183458742,245.748399198052
28.8106569672969,245.944940046435
28.62920526495,246.140805929649
28.4474825988409,246.336003260608
28.2654920614516,246.530538418826
28.0832367196421,246.724417750391
27.9007196150054,246.917647567959
27.7179437640725,247.110234150633
27.5349121592844,247.302183744456
27.351627768428,247.493502561723
27.1680935356087,247.684196781489
26.9843123814567,247.874272549499
26.8002872034847,248.063735978237
26.6160208764502,248.252593147001
26.4315162527175,248.440850101971
26.2467761626193,248.628512856292
26.0618034148215,248.815587390172
25.8766007966854,249.002079650975
25.6911710744875,249.187995553218
25.5055169943909,249.373340979155
25.3196412819078,249.558121778197
25.1335466428761,249.742343767509
24.9472357636841,249.926012732033
24.7607113116483,250.109134424634
24.5739759353916,250.29171456625
24.3870322652275,250.473758846047
24.1998829135445,250.655272921583
24.0125304751964,250.836262418978
23.8249775278977,251.016732933086
23.6372266324687,251.196690027559
23.4492803338395,251.3761392355
23.2611411605543,251.555086058946
23.0728116257874,251.733535969533
22.8842942276097,251.91149440858
22.6955914494105,252.088966787283
22.5067057603331,252.265958486932
22.3176396157075,252.44247485911
22.1283954575005,252.618521225919
21.9389757147672,252.794102880188
21.7493828041124,252.969225085699
21.5596191301667,253.143893077409
21.3696870859156,253.318112061559
21.1795890537908,253.491887216382
20.9893274052818,253.665223691618
20.7989045020488,253.838126609229
20.6083226963049,254.010601063518
20.4175843313608,254.182652121367
20.2266917421863,254.354284822481
20.0356472559898,254.525504179635
19.8444531928117,254.696315178917
19.6531118661401,254.866722779982
19.4616255835443,255.036731916297
19.2699966471853,255.206347495279
19.0782273550885,255.375574399022
18.8863200009595,255.544417483842
18.6942768755099,255.712881581003
18.5021002670717,255.880971496866
18.3097924623884,256.04869201314
18.1173557474417,256.216047887148
17.9247924083136,256.383043852086
17.7321047320825,256.549684617285
17.5392950077706,256.715974868478
17.3463655273249,256.881919268062
17.1533185865049,257.047522455245
16.960156486551,257.212789046788
16.7668815344444,257.377723636555
16.573496044693,257.542330796264
16.3800023404415,257.706615075624
16.1864027548039,257.870581002615
15.9926996322647,258.034233083748
15.7988953301585,258.197575804339
15.6049922202397,258.360613628777
15.4109926903391,258.523351000792
15.2168991461196,258.685792343727
15.0227140127987,258.847942060688
14.8284397377028,259.009804535292
14.6340787915045,259.171384131219
14.4396336710374,259.332685192964
14.2451069015342,259.493712045984
14.0505010391638,259.654468996969
13.8558186737402,259.814960334115
13.6610624316144,259.975190327393
13.4662349787613,260.135163228816
13.2713390240837,260.294883272716
13.0763773229446,260.454354676006
12.8813526809563,260.613581638456
12.686267957889,260.772568342839
12.4911260726026,260.931318955682
12.2959300068463,261.089837626816
12.1006828108515,261.24812849012
11.9053876085755,261.406195663677
11.7100476034878,261.564043250036
11.5146660848035,261.721675336486
11.3192464341765,261.879095995315
11.1237921329128,262.036309284085
10.9283067697327,262.193319245898
10.7327940491257,262.35012990966
10.537257800205,262.50674529023
10.3417019869672,262.66316938916
10.1461307178578,262.819406194249
9.950548257575,262.975459680283
9.75495903898821,263.131333809181
9.55936767612366,263.287032530259
9.36377897810584,263.442559780496
9.16819796411793,263.597919484791
8.97262987945744,263.753115556235
8.77708021270889,263.908151896369
8.5815547141292,264.063032395446
8.3860594151297,264.217760932573
8.19060064978912,264.372341376453
7.9951850763252,264.526777584927
7.79981970146249,264.681073405714
7.60451190569772,264.83523267655
7.40926947053906,264.989259225449
7.2141006079233,265.143156870961
7.01901399244219,265.296929422432
6.82401879741112,265.450580680265
6.6291247365674,265.604114436171
6.43434211441215,265.757534473436
6.23968189010315,265.91084456705
6.04515576423077,266.064048484447
5.85077630052058,266.217149985045
5.65655710894972,266.370152820978
5.46251312779289,266.523060737231
5.26866107205731,266.6758774719
5.07457435847045,266.828606756443
4.88132046854481,266.981252315938
4.68841926084009,267.133817869332
4.49586789871138,267.286307129701
4.30367089217433,267.438723804502
4.11184010736023,267.591071595823
3.92039477480039,267.743354200522
3.72936149734115,267.895575310952
3.53877425565189,268.047738614502
3.34867441406666,268.199847794324
3.15911072469523,268.351906529465
2.97013933063713,268.503918495123
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
        # - atm_corr = False below
        (
            40,
            -105,
            -6,
            noaa.datetimerange(
                datetime.datetime(2010, 6, 21, 0, 6),
                datetime.datetime(2010, 6, 21, 0, 24),
                6,
            ),
            False,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-25.245718494866,	345.86910228316
-25.5116570005578,	347.363394492955
-25.7482680271277,	348.866858015593
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
        (
            40,
            -105,
            -6,
            noaa.datetimerange(
                datetime.datetime(2010, 6, 21, 0, 6),
                datetime.datetime(2010, 6, 22, 0, 0),
                6,
            ),
            False,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-25.245718494866,345.86910228316
-25.5116570005578,347.363394492955
-25.7482680271277,348.866858015593
-25.9552183636807,350.378512732807
-26.1322125703073,351.897331655263
-26.2789949633587,353.422246027742
-26.395351369231,354.952150988432
-26.4811106191101,356.485911720329
-26.5361457604144,358.022370018731
-26.5603749650459,359.560351189686
-26.5537621191813,1.09867118388445
-26.5163170846795,2.63614386580969
-26.4480956276269,4.17158831262935
-26.3491990152519,5.70383603820096
-26.2197732880543,7.23173803789319
-26.060008219394,8.75417155641839
-25.8701359798672,10.2700464868082
-25.6504295283237,11.7783113192214
-25.401200755234,13.2779585697837
-25.1227984074212,14.7680296316671
-24.8156058253865,16.2476190058521
-24.4800385262635,17.7158778816055
-24.1165416659564,19.172017052416
-23.7255874143017,20.6153091650712
-23.3076722760517,22.0450903137511
-22.8633143894616,23.4607610007815
-22.3930508319689,24.8617864971123
-21.8974349605038,26.2476966422166
-21.3770338108249,27.6180851311283
-20.8324255778135,28.9726083395377
-20.2641971951019,30.3109837424229
-19.6729420297511,31.6329879818931
-19.0592577043583,32.9384546408456
-18.4237440559804,34.2272717779075
-17.7670012388415,35.4993792762134
-17.0896279746517,36.754766056848
-16.3922199526905,37.9934672027996
-15.6753683790617,39.2155610366279
-14.9396586734363,40.4211661893665
-14.1856693093531,41.6104386951088
-13.4139707936377,42.7835691399645
-12.6251247787212,43.9407798910859
-11.81968330166,45.0823224260528
-10.9981881422812,46.2084747803346
-10.161170293343,47.3195391257453
-9.3091495345565,48.4158394908254
-8.44263410301375,49.4977196301484
-7.56212045216107,50.5655410477247
-6.66809309160314,51.6196811774994
-5.76102450079274,52.6605317214901
-4.84137510914886,53.6884971456187
-3.90959333645129,54.7039933309497
-2.96611568679265,55.7074463782421
-2.01136689077707,56.6992915619059
-1.04576009010032,57.6799724300869
-0.0696970601015181,58.6499400462365
0.916431534696926,59.6096523684939
1.91224585556861,60.5595737622039
2.91737657920194,61.5001746421249
3.93146456460033,62.4319312401593
4.95416050054874,63.3553254958562
5.98512453559836,64.2708450665604
7.02402589272836,65.1789834552292
8.07054247049445,66.0802402546079
9.1243604315022,66.9751215066672
10.1851737796913,67.8641401778856
11.2526839264721,68.7478167509043
12.3265992465711,69.626679935014
13.4066346229782,70.5012674980387
14.4925109812219,71.3721272242726
15.5839548117196,72.2398180034306
16.6806976797897,73.1049110578651
17.7824757213978,73.9679913158527
18.8890291235368,74.8296589413109
20.0001015865759,75.690531031177
21.1154397666799,76.5512434945695
22.2347926949153,77.4124531292592
23.3579111698228,78.2748399139376
24.4845471197059,79.1391095375199
25.614452929609,80.0059961893104
26.7473807283473,80.8762656381351
27.883081628968,81.750718631559
29.0213049163684,82.6301946516568
30.1617971735481,83.5155760678931
31.3043013380395,84.4077927342678
32.4485556774745,85.307827083391
33.594292672918,86.2167197783725
34.7412377955385,87.13557599074
35.8891081613172,88.0655723828968
37.0376110447719,89.0079648832434
38.1864422310197,89.9640973549392
39.3352841810245,90.9354112718009
40.4838039815991,91.9234565302718
41.631651047089,92.9299035429489
42.7784545335244,93.956556776723
43.9238204207392,95.0053699191154
45.0673282092166,96.0784628761842
46.2085271708989,97.1781408279001
47.3469320816803,98.3069155869589
48.4820183525921,99.4675295274201
49.6132164615592,100.662982363516
50.7399055728491,101.896561067381
51.8614062117936,103.171873207295
52.9769718429482,104.492883962128
54.0857791756943,105.86395700678
55.1869169977298,107.289899356044
56.2793733100687,108.776010072348
57.3620205128128,110.328132458083
58.4335983695194,111.952708918206
59.4926944642348,113.656837032353
60.5377218690074,115.44832444001
61.566893768429,117.335738807647
62.5781948630306,119.328447290672
63.5693495150489,121.43663737
64.5377868472005,123.67130758917
65.4806033991326,126.044212421207
66.3945245500077,128.567740264205
67.2758667920966,131.254697646958
68.1205041592603,134.117966859036
68.9238437111637,137.169999908703
69.6808169217643,140.422111632585
70.3858959410358,143.883543012358
71.0331455830363,147.560287671097
71.6163227963606,151.453715632978
72.1290341992863,155.559091611348
72.5649577292231,159.864165906024
72.9181255707518,164.348097266033
73.1832524124327,168.981016568875
73.3560778629642,173.724516981045
73.4336789718744,178.533230037882
73.4147039347264,183.3574244066
73.2994855658027,188.146304468253
73.0900130418189,192.851486254074
72.7897673517007,197.430075203458
72.4034510130718,201.846887993571
71.9366580164717,206.075596047525
71.3955323094227,210.09882372923
70.7864544572001,213.907423165796
70.1157816635051,217.499231602807
69.3896515341766,220.877607092995
68.6138483860466,224.049971675359
67.7937237947122,227.026507070503
66.9341600086994,229.819072793473
66.0395646490314,232.440362057604
65.1138865123106,234.903277840968
64.1606443417091,237.220495626809
63.1829625158432,239.40417494219
62.1836094272407,241.465783962096
61.1650357685512,243.416006615861
60.1294110230855,245.264707646808
59.0786572166713,247.020936780467
58.0144795022999,248.692958031527
56.9383934788092,250.288294098692
55.8517493455314,251.813778811829
54.7557531078102,253.275612843321
53.6514851016284,254.679419532228
52.539916124233,256.030298831681
51.4219214519112,257.332878203311
50.2982930101206,258.591359835343
49.1697499367457,259.809563932717
48.0369477548217,260.990968065823
46.9004863443992,262.138742715166
45.760916880262,263.255783234857
44.6187478789819,264.34473850451
43.474450480237,265.408036555417
42.3284630687786,266.447907458186
41.1811953293156,267.466403747037
40.0330318128392,268.465418639567
38.8843350816379,269.446702290497
37.7354484912463,270.411876295845
36.5866986582801,271.362446643728
35.4383976572309,272.299815286409
34.2908449821073,273.225290490338
33.1443293048727,274.140096102247
31.9991300570834,275.045379854608
30.8555188585942,275.942220818357
29.7137608128343,276.831636099089
28.5741156866271,277.714586860496
27.4368389890175,278.591983749817
26.3021829627555,279.464691790065
25.1703974992166,280.333534797028
24.0417309870848,281.199299371095
22.9164311032113,282.062738508498
21.7947455529597,282.924574871073
20.6769227670167,283.78550374836
19.5632125598018,284.646195742523
18.4538667550018,285.507299201812
17.3491397819631,286.36944242603
16.249289247235,287.233235663445
15.1545764839045,288.099272917031
14.0652670820281,288.968133574496
12.9816314019115,289.840383875501
11.9039450727143,290.716578226499
10.8324894773774,291.597260372981
9.76755222562748,292.482964436247
8.70942761539668,293.374215821478
7.65841708363156,294.271532001601
6.61482964654208,295.175423180854
5.57898232904047,296.086392840823
4.55120058336522,297.004938170129
3.53181869564959,297.931550378917
2.52118017988005,298.866714897418
1.5196381573174,299.810911458071
0.527555720118102,300.764614058952
-0.454693723488433,301.72829080667
-1.42672612449333,302.70240363522
-2.38814649228797,303.687407897955
-3.33854862058199,304.683751828306
-4.27751484430003,305.691875865777
-5.2046158311871,306.712211842429
-6.11941041321747,307.74518202626
-7.02144546253919,308.791198016969
-7.91025581764157,309.850659490654
-8.78536426585164,310.923952790492
-9.64628158821569,312.011449360636
-10.4925066739617,313.113504022617
-11.3235267112523,314.230453093694
-12.1388174620592,315.362612349445
-12.9378436283996,316.510274833584
-13.7200593180954,317.673708521563
-14.4849086174621,318.853153845854
-15.2318262789782,320.048821095131
-15.9602385309833,321.260887701559
-16.6695640167256,322.489495435436
-17.3592148687441,323.734747529018
-18.0285979243708,324.996705756898
-18.6771160864563,326.275387503495
-19.3041698324283,327.570762853373
-19.9091588731351,328.882751744546
-20.4914839607292,330.211221228331
-21.0505488431598,331.555982884498
-21.5857623598883,332.91679044237
-22.0965406712952,334.293337662685
-22.5823096109069,335.685256535309
-23.0425071470208,337.09211585005
-23.4765859367912,338.513420195657
-23.8840159531309,339.948609441546
-24.2642871613908,341.397058751514
-24.6169122202573,342.858079174853
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            noaa.datetimerange(
                datetime.datetime(2023, 9, 21, 5, 33),
                datetime.datetime(2023, 9, 21, 5, 36),
                1,
            ),
            False,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-5.24086479367834,	85.1264242410581
-5.0431309990811,	85.2800907071635
-4.84535333099088,	85.4336534862891
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            noaa.datetimerange(
                datetime.datetime(2023, 9, 21, 5, 33),
                datetime.datetime(2023, 9, 21, 17, 50),
                1,
            ),
            False,
            [
                (float(row[0]), float(row[1]))
                for row in csv.reader(
                    StringIO(
                        """-5.24086479367834,85.1264242410581
-5.0431309990811,85.2800907071635
-4.84535333099088,85.4336534862891
-4.64753324187292,85.5871163110677
-4.44967218068956,85.7404829080009
-4.25177159303308,85.8937569977111
-4.05383292124972,86.0469422951765
-3.85585760457462,86.2000425099902
-3.65784707925711,86.3530613465979
-3.45980277868988,86.5060025045469
-3.26172613353974,86.6588696787374
-3.06361857194783,86.811666559827
-2.86548151935138,86.9643968338112
-2.66731639907502,87.1170641832801
-2.46912463214588,87.269672286986
-2.27090763750024,87.4222248202637
-2.07266683210781,87.5747254552722
-1.87440363109863,87.7271778612431
-1.67611944789039,87.8795857047292
-1.47781569431038,88.0319526498428
-1.27949378072677,88.1842823585149
-1.0811551161685,88.3365784907289
-0.882801108530629,88.4888447049431
-0.684433164390228,88.6410846576603
-0.486052689593848,88.7933020046859
-0.287661089075058,88.9455004007024
-0.0892597670553954,89.0976834996826
0.109149872831225,89.2498549551361
0.307566427412851,89.4020184203577
0.505988493855526,89.554177548673
0.704414669537627,89.7063359936884
0.902843551925443,89.8584974095368
1.10127373845073,90.0106654511214
1.29970382630502,90.1628437745391
1.4981324126254,90.3150360366499
1.69655809390748,90.4672458963357
1.89497946618766,90.6194770140759
2.09339512484149,90.7717330523639
2.29180366445884,90.9240176759545
2.49020367871624,91.0763345521179
2.68859376025495,91.2286873508808
2.88697250055291,91.3810797452811
3.08533848979937,91.5335154116161
3.28369031676957,91.6859980296911
3.48202656861814,91.8385312832439
3.68034583106689,91.9911188595091
3.87864668780895,92.1437644504934
4.07692772069436,92.2964717525431
4.27518750952409,92.4492444667673
4.47342463192138,92.6020862992909
4.6716376632059,92.7550009615025
4.86982517626271,92.9079921703114
5.06798574141585,93.0610636483957
5.26611792629808,93.2142191244571
5.46422029572034,93.3674623334768
5.66229141154373,93.520797016964
5.86032983247014,93.674226923383
6.05833411422226,93.8277558077283
6.25630280894596,93.9813874327975
6.45423446538922,94.1351255687679
6.65212762869275,94.2889739936201
6.84998084025631,94.4429364933956
7.04779263760567,94.5970168624524
7.24556155425775,94.7512189037234
7.44328611958666,94.9055464289722
7.6409648586891,95.0600032590499
7.83859629224752,95.2145932241545
8.0361789363163,95.3693201642585
8.23371130249542,95.5241879286906
8.43119189732654,95.6792003774104
8.62861922246515,95.8343613805915
8.82599177446407,95.9896748190499
9.02330804463253,96.1451445845071
9.22056651889608,96.3007745798498
9.41776567765589,96.4565687193895
9.61490399564538,96.6125309291273
9.81197994178793,96.7686651470145
10.008991979052,96.9249753232176
10.2059385642279,97.0814654205511
10.4028181480995,97.238139414055
10.5996291748214,97.39500129229
10.7963700820899,97.5520550569126
10.9930393009134,97.709304723116
11.1896352554651,97.8667543198912
11.3861563629326,98.0244078902944
11.5826010333647,98.1822694917151
11.7789676695224,98.3403431961381
11.9752546667226,98.4986330904156
12.1714604126867,98.6571432765296
12.3675832873037,98.8158778720334
12.5636216627931,98.9748410096336
12.7595739030704,99.1340368384852
12.9554383639052,99.2934695237774
13.1512133926834,99.4531432471715
13.3468973282465,99.6130622070692
13.5424885007286,99.773230618883
13.7379852313944,99.9336527153052
13.9333858324733,100.094332746579
14.1286886069944,100.255274980767
14.3238918486206,100.416483704018
14.5189938414794,100.577963220844
14.7139928599129,100.739717854557
14.9088871686295,100.90175194685
15.1036750220485,101.064069859106
15.2983546644492,101.226675971972
15.4929243297149,101.389574685807
15.6873822411569,101.552770420949
15.8817266113366,101.716267617989
16.0759556418878,101.880070738033
16.2700675233348,102.044184262978
16.4640604349116,102.20861269578
16.6579325443761,102.373360560725
16.8516820077463,102.538432403863
17.0453069694405,102.703832792593
17.2388055615969,102.869566316964
17.4321759042127,103.03563758925
17.6254161048697,103.202051244396
17.8185242585436,103.368811940276
18.0114984474076,103.535924357962
18.2043367406379,103.70339320199
18.3970371942158,103.871223200622
18.5895978507268,104.039419106109
18.782016739162,104.207985694954
18.9742918746302,104.376927768348
19.1664212584875,104.54625015173
19.3584028776324,104.715957696092
19.550234704627,104.886055277546
19.7419146974087,105.056547797743
19.9334407990762,105.227440184134
20.1248109376767,105.398737390225
20.3160230259908,105.570444395823
20.5070749613138,105.742566207291
20.6979646252398,105.91510785779
20.8886898834389,106.08807440753
21.07924858535,106.261470944187
21.2696385642963,106.43530258244
21.4598576367492,106.609574465268
21.6499036024378,106.784291763482
21.8397742440378,106.959459676133
22.0294673269344,107.135083430747
22.2189805989903,107.311168283552
22.4083117903102,107.487719519703
22.5974586130011,107.664742453503
22.7864187609328,107.842242428625
22.9751899094947,108.020224818326
23.1637697153519,108.19869502566
23.3521558161121,108.377658483863
23.5403458304267,108.557120655844
23.7283373572149,108.737087035456
23.9161279757625,108.917563146977
24.103715245376,109.098554545485
24.291096705133,109.280066817032
24.4782698736159,109.462105578841
24.6652322486564,109.644676479469
24.8519813070713,109.827785198986
25.0385145043942,110.011437449141
25.2248292746155,110.195638973513
25.4109230298161,110.380395547854
25.5967931602604,110.565712979513
25.782437033584,110.751597108653
25.9678519948729,110.938053807673
26.1530353663027,111.125088981506
26.3379844468558,111.312708567744
26.5226965120393,111.50091853675
26.7071688136044,111.689724891757
26.8913985792576,111.879133668973
27.0753830123763,112.069150937658
27.2591192917176,112.259782800209
27.4426045710338,112.451035392409
27.6258359791504,112.642914882761
27.8088106191159,112.835427473627
27.9915255682721,113.028579400543
28.1739778778666,113.222376932426
28.3561645727471,113.416826371598
28.5380826510612,113.611934053792
28.7197290839522,113.80770634814
28.90110081525,114.004149657172
29.0821947611671,114.201270416768
29.2630078099839,114.399075096134
29.4435368216444,114.597570197917
29.6237786278246,114.796762257414
29.8037300310449,114.996657843578
29.9833878047355,115.197263558195
30.1627486928235,115.398586035948
30.3418094094108,115.600631944299
30.5205666384585,115.803407983334
30.6990170334613,116.006920885607
30.8771572171261,116.211177415959
31.0549837810457,116.416184371327
31.2324932853743,116.621948580527
31.4096822585035,116.828476904017
31.5865471966313,117.03577623384
31.7630845638317,117.243853492602
31.9392907911326,117.452715634298
32.1151622765808,117.662369643251
32.2906953848122,117.872822533966
32.4658864467218,118.084081350772
32.6407317591303,118.296153167442
32.8152275844532,118.509045086788
32.9893701503701,118.722764240233
33.1631556494907,118.937317787357
33.3365802390236,119.152712915416
33.5096400403408,119.368956839031
33.6823311390565,119.5860567989
33.8546495840811,119.804020062363
34.0265913877008,120.022853922063
34.1981525251439,120.242565695517
34.3693289342522,120.463162724467
34.5401165151514,120.684652374203
34.7105111299266,120.907042032846
34.8805086022934,121.130339110613
35.050104717277,121.354551039032
35.2192952208857,121.579685270139
35.3880758196883,121.805749275813
35.5564421809152,122.03275054615
35.72438993151,122.260696589666
35.8919146582381,122.48959493159
36.0590119072665,122.719453113065
36.2256771838607,122.950278690104
36.391905952076,123.182079232521
36.5576936344568,123.414862322817
36.7230356117393,123.648635555018
36.8879272225537,123.883406533482
37.0523637631392,124.119182871645
37.2163404869456,124.355972190927
37.3798526047905,124.593782118639
37.5428952839281,124.832620287734
37.7054636482138,125.072494334621
37.8675527777319,125.313411897874
38.0291577085359,125.555380616704
38.1902734323932,125.798408129381
38.350894896543,126.042502071596
38.5110170034519,126.287670074786
38.6706346105857,126.533919764385
38.8297425301828,126.781258758041
38.9883355290364,127.029694663761
39.1464083281748,127.279235078194
39.3039556031161,127.529887583917
39.4609719829935,127.781659748543
39.617452050832,128.034559121883
39.7733903432624,128.288593233995
39.9287813503596,128.543769592979
40.0836195154962,128.800095682712
40.2378992352004,129.057578960518
40.3916148590323,129.316226854772
40.5447606894689,129.576046762442
40.6973309818007,129.83704604657
40.8493199439272,130.099232033858
41.0007217367547,130.362612011264
41.151530473426,130.627193224399
41.3017402197482,130.892982873976
41.451344994041,131.159988113142
41.6003387671272,131.428216044524
41.7487154623308,131.697673717231
41.896468955497,131.96836812377
42.0435930750287,132.240306196894
42.1900816019373,132.513494806378
42.3359282699214,132.787940755714
42.4811267653317,133.063650778928
42.6256707277772,133.340631536384
42.7695537495196,133.618889612383
42.9127693761167,133.898431510823
43.0553111064786,134.179263651707
43.1971723930637,134.4613923674
43.3383466420987,134.744823898806
43.4788272138245,135.029564391474
43.6186074227657,135.315619891619
43.7576805380239,135.60299634208
43.8960397835978,135.891699578198
44.0336783385991,136.181735323807
44.1705893381421,136.473109186216
44.3067658729722,136.76582665299
44.4422009904101,137.059893086785
44.5768876946806,137.355313721049
44.710818947402,137.652093655463
44.8439876681022,137.950237851321
44.9763867347724,138.249751126821
45.1080089844445,138.550638152316
45.238847213809,138.852903445473
45.3688941798606,139.156551366383
45.4981426005779,139.461586112608
45.626585155509,139.768011714336
45.7542144870533,140.075832028583
45.8810232004516,140.385050735145
46.0070038651377,140.695671330685
46.1321490154688,141.007697123671
46.2564511516245,141.321131229081
46.3799027405412,141.635976563065
46.5024962168895,141.952235837563
46.6242239840874,142.269911554875
46.7450784153563,142.589006002202
46.8650518548184,142.909521246144
46.9841366184924,143.231459127347
47.1023249960309,143.554821254235
47.2196092511039,143.8796089985
47.3359816232194,144.205823488785
47.4514343288954,144.533465605245
47.5659595630012,144.862535973925
47.6795495001591,145.193034961125
47.7921962961766,145.524962667767
47.9038920895326,145.858318923762
48.0146290029024,146.193103282393
48.1243991447284,146.52931501471
48.2331946106946,146.866953104113
48.3410074859672,147.206016240098
48.4478298460313,147.54650281378
48.5536537590259,147.888410911696
48.6584712873959,148.23173831054
48.7622744897335,148.576482471774
48.8650554226715,148.922640536281
48.9668061428122,149.270209319104
49.0675187087101,149.619185304239
49.1671851828933,149.96956463952
49.265797633932,150.32134313158
49.3633481383972,150.674516241084
49.4598287836218,151.029079077214
49.5552316689911,151.38502639395
49.6495489087922,151.74235258478
49.742772634335,152.101051678389
49.8348949962856,152.461117334296
49.9259081670255,152.822542838647
50.015804343052,153.185321100147
50.1045757474281,153.549444646156
50.1922146322491,153.914905618951
50.2787132811698,154.281695772156
50.3640640119489,154.649806467365
50.448259178879,155.019228671102
50.5312911760305,155.389952951208
50.613152438961,155.761969474997
50.6938354480198,156.135268006058
50.773332730904,156.509837902074
50.8516368653846,156.88566811271
50.9287404820738,157.262747177744
51.004636267203,157.64106322545
51.079316965429,158.020603971231
51.1527753826628,158.401356716518
51.2250043889033,158.78330834795
51.2959969209414,159.166445336959
51.3657459858723,159.55075373894
51.4342446630133,159.936219194138
51.5014861074392,160.322826927409
51.5674635527216,160.710561748987
51.6321703138262,161.099408055444
51.6955997900291,161.489349830938
51.7577454678098,161.880370648813
51.8186009237602,162.272453673501
51.8781598274785,162.665581662767
51.9364159444539,163.059736970296
51.9933631387814,163.454901548737
52.0489953766856,163.851056952441
52.1033067283719,164.248184341861
52.1562913715168,164.646264486973
52.2079435939036,165.045277771723
52.2582577962059,165.445204198671
52.3072284947362,165.846023394007
52.3548503241641,166.247714612904
52.4011180402068,166.650256745229
52.4460265222736,167.053628321605
52.4895707760792,167.457807519817
52.5317459360373,167.862772171688
52.5725472684672,168.268499769706
52.6119701730406,168.67496747517
52.6500101858824,169.082152125504
52.686662981774,169.490030242472
52.721924376459,169.898578040625
52.7557903288938,170.307771436058
52.7882569434364,170.717586055479
52.8193204719666,171.1279972456
52.8489773159418,171.538980082815
52.8772240283821,171.950509383175
52.9040573157807,172.362559712654
52.929474039761,172.775105397781
52.9534712195417,173.188120536044
52.9760460325584,173.601579007542
52.9971958167626,174.015454485889
53.0169180719558,174.429720449842
53.0352104612157,174.844350195061
53.0520708122354,175.259316846067
53.0674971185673,175.674593368401
53.0814875407804,176.090152580968
53.0940404075234,176.505967168545
53.1051542164867,176.92200969445
53.1148276351043,177.338252613427
53.1230595020386,177.754668284261
53.1298488267847,178.171228983308
53.1351947909646,178.587906917313
53.1390967486229,179.004674236717
53.1415542266094,179.421503048947
53.1425669248494,179.83836543176
53.1421347165238,180.255233446629
53.1402576481399,180.672079152112
53.1369359395008,181.088874617276
53.1321699835796,181.505591935075
53.1259603461027,181.922203235776
53.1183077659456,182.338680700019
53.1092131536066,182.754996572449
53.098677591401,183.171123174648
53.086702332648,183.587032918283
53.073288800936,184.002698318095
53.0584385892954,184.418092004762
53.0421534592703,184.833186737626
53.0244353398989,185.247955417276
53.0052863266004,185.662371097962
52.9847086799657,186.076406999834
52.9627048242772,186.490036521032
52.9392773468543,186.903233249366
52.9144289954821,187.315970974197
52.8881626775834,187.728223697671
52.8604814583956,188.13996564592
52.8313885592444,188.551171279979
52.8008873557443,188.961815306435
52.7689813759216,189.371872687806
52.7356742982599,189.781318652648
52.700969949678,190.190128705355
52.6648723034347,190.598278635683
52.6273854769713,191.00574452795
52.5885137295047,191.412502769958
52.5482614604819,191.818530061484
52.5066332061285,192.223803422658
52.4636336377884,192.628300201799
52.4192675592929,193.031998083025
52.3735399044577,193.434875093496
52.3264557345347,193.836909610322
52.2780202356253,194.238080367123
52.2282387160428,194.638366460235
52.1771166036475,195.037747354574
52.1246594431388,195.436202889147
52.0708728931296,195.833713282208
52.0157627241298,196.230259136064
51.9593348146269,196.625821441535
51.9015951490236,197.02038158206
51.8425498146078,197.413921337448
51.782204998699,197.806422887292
51.7205669857782,198.197868814039
51.6576421546032,198.58824210571
51.5934369753174,198.977526158294
51.5279580065523,199.365704777799
51.461211892522,199.75276218198
51.393205359934,200.138683001724
51.3239452158231,200.523452282193
51.2534383435438,200.907055483503
51.1816917006137,201.289478481242
51.108712315639,201.670707566615
51.0345072854434,202.050729446305
50.9590837721982,202.429531242047
50.8824490005779,202.807100489921
50.8046102549255,203.183425139365
50.7255748764408,203.558493551931
50.645350260382,203.932294499769
50.5639438531201,204.304817163833
50.4813631501251,204.676051132005
50.3976156921414,205.045986396659
50.3127090632344,205.414613352317
50.2266508879414,205.781922792926
50.1394488286445,206.147905908956
50.0511105829659,206.512554284293
49.961643881207,206.875859892939
49.8710564838151,207.237815095525
49.7793561788867,207.598412635644
49.6865507797132,207.957645636015
49.5926481223596,208.315507594492
49.497656063097,208.671992379857
49.4015824768028,209.027094227724
49.3044352535493,209.380807735819
49.2062222970893,209.733127859612
49.1069515224507,210.084049907586
49.0066308537604,210.433569536448
48.9052682221222,210.78168274623
48.8028715635172,211.128385875291
48.6994488167731,211.473675595238
48.5950079215591,211.817548905758
48.4895568164351,212.160003129376
48.3831034367589,212.501035906084
48.2756557135524,212.840645188217
48.1672215705902,213.178829234663
48.0578089233602,213.515586605639
47.9474256771457,213.850916157109
47.8360797253485,214.184817035246
47.7237789478531,214.517288670854
47.6105312094325,214.848330773767
47.4963443582035,215.177943327238
47.3812262241223,215.506126582311
47.2651846175292,215.832881052184
47.1482273275574,216.158207506513
47.0303621214782,216.482106966057
46.9115967423017,216.804580696639
46.7919389082113,217.125630203817
46.6713963111426,217.445257227222
46.5499766155909,217.763463734995
46.4276874574499,218.080251918239
46.3045364429034,218.39562418551
46.1805311473493,218.709583157336
46.0556791143654,219.022131660774
45.9299878547206,219.333272724009
45.8034648452398,219.643009570913
45.6761175285998,219.951345616053
45.5479533113898,220.258284458947
45.4189795639769,220.563829879171
45.2892036195303,220.867985831117
45.1586327732527,221.170756438896
45.0272742816468,221.47214599129
44.8951353618236,221.772158936769
44.7622231908347,222.07079987857
44.6285449050483,222.368073569839
44.4941075995512,222.663984908839
44.3589183275827,222.958538934224
44.2229840998321,223.251740820293
44.0863118846323,223.543595872759
43.9489086064402,223.834109523697
43.810781146096,224.123287327454
43.6719363402334,224.411134956186
43.5323809808918,224.697658195558
43.3921218151636,224.982862940513
43.251165544856,225.266755191123
43.1095188261942,225.549341048508
42.9671882695319,225.83062671083
42.8241804391011,226.110618469364
42.6805018526094,226.389322704549
42.5361589817164,226.666745882591
42.3911582508194,226.942894551184
42.245506037574,227.217775336263
42.0992086725856,227.491394938356
41.9522724392819,227.763760129103
41.8047035738171,228.034877747848
41.656508264988,228.304754698314
41.5076926541693,228.573397945338
41.3582628352736,228.840814511693
41.2082248547225,229.107011474971
41.0575847112664,229.371995964443
40.9063483566729,229.635775158499
40.7545216947295,229.89835628114
40.6021105819642,230.159746599556
40.449120827528,230.419953421269
40.2955581932612,230.67898409144
40.1414283937801,230.936845990254
39.9867370965675,231.19354653036
39.8314899220855,231.449093154389
39.6756924438944,231.703493332527
39.5193501887865,231.956754560164
39.3624686367615,232.208884355488
39.2050532218534,232.459890257683
39.0471093312905,232.70977982412
38.8886423063442,232.95856062868
38.7296574423447,233.206240259594
38.5701599888783,233.452826317458
38.4101551499893,233.698326413301
38.2496480843942,233.942748166712
38.0886439057043,234.186099204022
37.9271476826524,234.428387156548
37.7651644393276,234.669619658874
37.602699155422,234.90980434721
37.4397567663141,235.148948857669
37.2763421639819,235.38706082516
37.1124601962819,235.624147881232
36.9481156678678,235.860217653052
36.7833133403105,236.095277761905
36.6180579323657,236.329335821828
36.4523541202641,236.562399438305
36.286206537998,236.794476207002
36.1196197776082,237.025573712548
35.9525983894907,237.25569952736
35.7851468826856,237.484861210509
35.6172697250263,237.713066306513
35.4489713440902,237.94032234474
35.2802561265362,238.166636837719
35.1111284190682,238.392017280619
34.9415925285863,238.616471150201
34.771652722502,238.840005903921
34.6013132290628,239.06262897907
34.4305782376681,239.284347791945
34.2594518991971,239.505169737061
34.0879383263317,239.725102186393
33.9160415938811,239.944152488647
33.7437657389531,240.16232796846
33.5711147619192,240.379635926189
33.3980926257849,240.596083636598
33.2247032571617,240.811678348713
33.0509505464366,241.026427285135
32.8768383481018,241.240337641493
32.70237048109,241.453416585932
32.5275507291019,241.665671258619
32.352382840942,241.877108771278
32.1768705308486,242.087736206755
32.001017478824,242.2975606186
31.8248273308115,242.506589030559
31.6483036996542,242.714828436676
31.4714501644818,242.922285800246
31.2942702716683,243.128968053963
31.1167675350057,243.334882099495
30.9389454360327,243.540034807208
30.7608074243614,243.744433015906
30.5823569180042,243.948083532586
30.4035973037002,244.150993132221
30.2245319372351,244.353168557549
30.0451641437745,244.554616518898
29.8654972181752,244.755343694005
29.6855344251581,244.955356727759
29.5052790002466,245.154662232526
29.3247341491506,245.35326678733
29.1439030487095,245.551176938219
28.9627888470465,245.748399198052
28.7813946638873,245.944940046435
28.5997235908674,246.140805929649
28.4177786918461,246.336003260608
28.2355630032135,246.530538418826
28.053079534198,246.724417750391
27.8703312671702,246.917647567959
27.6873211577933,247.110234150633
27.5040521359403,247.302183744456
27.3205271050709,247.493502561723
27.1367489431433,247.684196781489
26.9527205027581,247.874272549499
26.7684446114496,248.063735978237
26.5839240719796,248.252593147001
26.3991616626283,248.440850101971
26.2141601374806,248.628512856292
26.0289222267134,248.815587390172
25.8434506368772,249.002079650975
25.6577480510298,249.187995553218
25.4718171296212,249.373340979155
25.2856605098619,249.558121778197
25.0992808066038,249.742343767509
24.912680612464,249.926012732033
24.7258624980972,250.109134424634
24.5388290124638,250.29171456625
24.3515826830986,250.473758846047
24.1641260163746,250.655272921583
23.9764614977673,250.836262418978
23.7885915921178,251.016732933086
23.6005187437394,251.196690027559
23.4122453772774,251.3761392355
23.2237738970602,251.555086058946
23.0351066879569,251.733535969533
22.8462461154765,251.91149440858
22.6571945260148,252.088966787283
22.4679542471055,252.265958486932
22.2785275876605,252.44247485911
22.088916838217,252.618521225919
21.8991242711759,252.794102880188
21.7091521410394,252.969225085699
21.5190026846522,253.143893077409
21.3286781212819,253.318112061559
21.138180653452,253.491887216382
20.9475124662769,253.665223691618
20.7566757282875,253.838126609229
20.5656725915091,254.010601063518
20.3745051916852,254.182652121367
20.1831756485017,254.354284822481
19.9916860658091,254.525504179635
19.8000385318405,254.696315178917
19.6082351194299,254.866722779982
19.4162778862262,255.036731916297
19.2241688747602,255.206347495279
19.0319101132505,255.375574399022
18.8395036149214,255.544417483842
18.6469513788061,255.712881581003
18.4542553898056,255.880971496866
18.2614176188923,256.04869201314
18.0684400233135,256.216047887148
17.875324546794,256.383043852086
17.6820731197312,256.549684617285
17.4886876593998,256.715974868478
17.2951700701437,256.881919268062
17.1015222434256,257.047522455245
16.9077460586061,257.212789046788
16.7138433822542,257.377723636555
16.519816068927,257.542330796264
16.3256659612072,257.706615075624
16.1313948898934,257.870581002615
15.937004674184,258.034233083748
15.7424971218589,258.197575804339
15.5478740294651,258.360613628777
15.353137182496,258.523351000792
15.1582883555684,258.685792343727
14.9633293124594,258.847942060688
14.7682618068598,259.009804535292
14.5730875816802,259.171384131219
14.3778083698045,259.332685192964
14.1824258941174,259.493712045984
13.9869418676741,259.654468996969
13.7913579938708,259.814960334115
13.5956759666139,259.975190327393
13.3998974704857,260.135163228816
13.2040241809109,260.294883272716
13.0080577643193,260.454354676006
12.8119998783126,260.613581638456
12.615852171677,260.772568342839
12.4196162851293,260.931318955682
12.2232938506016,261.089837626816
12.0268864919821,261.24812849012
11.8303958251296,261.406195663677
11.6338234580248,261.564043250036
11.4371709909326,261.721675336486
11.2404400165489,261.879095995315
11.0436321201579,262.036309284085
10.8467488797845,262.193319245898
10.6497918663438,262.35012990966
10.4527626436481,262.50674529023
10.2556627691328,262.66316938916
10.0584937931357,262.819406194249
9.86125725962998,262.975459680283
9.66395470621633,263.131333809181
9.4665876642751,263.287032530259
9.26915765910951,263.442559780496
9.07166621008449,263.597919484791
8.87411483077963,263.753115556235
8.67650502912063,263.908151896369
8.47883830752853,264.063032395446
8.2811161629112,264.217760932573
8.08334008738098,264.372341376453
7.88551156753094,264.526777584927
7.68763208514797,264.681073405714
7.48970311720457,264.83523267655
7.29172613599997,264.989259225449
7.09370260929158,265.143156870961
6.89563400043478,265.296929422432
6.69752176851586,265.450580680265
6.4993673684851,265.604114436171
6.30117225129411,265.757534473436
6.10293786388174,265.91084456705
5.90466564988249,266.064048484447
5.70635704889831,266.217149985045
5.50801349720352,266.370152820978
5.30963642773034,266.523060737231
5.11122727020359,266.6758774719
4.9127874512656,266.828606756443
4.71431839461265,266.981252315938
4.51582152111696,267.133817869332
4.31729824895922,267.286307129701
4.11874999375846,267.438723804502
3.92017816869515,267.591071595823
3.72158418450319,267.743354200522
3.52296945016089,267.895575310952
3.32433537216511,268.047738614502
3.12568335522994,268.199847794324
2.92701480226827,268.351906529465
2.72833111451938,268.503918495123
"""
                    )
                )
            ],
        ),  # latitude, longitude, timezone, thedates, atm_corr, expected
        # expected is saved from spreadsheet
    ],
)
def test_sunpositions(latitude, longitude, timezone, thedates, atm_corr, expected):
    result = noaa.sunpositions(latitude, longitude, timezone, thedates, atm_corr)
    for (r1, r2), (e1, e2) in zip(result, expected):
        assert almostequal(r1, e1)
        assert almostequal(r2, e2)


@pytest.mark.parametrize(
    "latitude, longitude, timezone, thedate, expected",
    [
        (
            40,
            -105,
            -6,
            datetime.datetime(2010, 6, 21),
            datetime.datetime(2010, 6, 21, 5, 31, 15, 842680),
        ),  # latitude, longitude, timezone, thedate, expected
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            datetime.datetime(2023, 9, 21),
            datetime.datetime(2023, 9, 21, 5, 55, 2, 693853),
        ),  # latitude, longitude, timezone, thedate, expected
    ],
)
def test_sunrise(latitude, longitude, timezone, thedate, expected):
    result = noaa.sunrise(latitude, longitude, timezone, thedate)
    assert result == expected


@pytest.mark.parametrize(
    "latitude, longitude, timezone, thedate, expected",
    [
        (
            40,
            -105,
            -6,
            datetime.datetime(2010, 6, 21),
            datetime.datetime(2010, 6, 21, 20, 32, 8, 805539),
        ),  # latitude, longitude, timezone, thedate, expected
    ],
)
def test_sunset(latitude, longitude, timezone, thedate, expected):
    result = noaa.sunset(latitude, longitude, timezone, thedate)
    assert result == expected
