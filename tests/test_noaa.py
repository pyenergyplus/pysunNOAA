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
    almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
        (0.104688683550086, 4126.22229222893),  # juliancentury_value, expected
        (0.23720916, 8896.83359556751),  # juliancentury_value, expected
    ],
)
def test_geom_mean_anom_sun_deg(juliancentury_value, expected):
    result = noaa.geom_mean_anom_sun_deg(juliancentury_value)
    almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
        (0.104688683550086, 0.016704231813213),  # juliancentury_value, expected
        (0.23720916, 0.0166986553093454),  # juliancentury_value, expected
    ],
)
def test_ent_earth_orbit(juliancentury_value, expected):
    result = noaa.eccent_earth_orbit(juliancentury_value)
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


@pytest.mark.parametrize(
    "juliancentury_value, expected",
    [
        (0.10468868, 23.4379297208038),  # juliancentury_value, expected
        (0.23720916, 23.4362064011546),  # juliancentury_value, expected
    ],
)
def test_mean_obliq_ecliptic_deg(juliancentury_value, expected):
    result = noaa.mean_obliq_ecliptic_deg(juliancentury_value)
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    print(sun_app_long_deg_value, mean_obliq_ecliptic_deg_value)
    result = noaa.sun_rt_ascen_deg(
        sun_app_long_deg_value, mean_obliq_ecliptic_deg_value
    )
    almostequal(result, expected)


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
    almostequal(result, expected)


@pytest.mark.parametrize(
    "obliq_corr_deg_value, expected",
    [
        (23.4384863293544, 0.0430314901072543),  # obliq_corr_deg_value, expected
        (23.4385024897594, 0.0430315511340247),  # obliq_corr_deg_value, expected
    ],
)
def test_var_y(obliq_corr_deg_value, expected):
    result = noaa.var_y(obliq_corr_deg_value)
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


@pytest.mark.parametrize(
    "true_solar_time_min_value, expected",
    [
        (1384.29369215928, 166.073423039819),  # true_solar_time_min_value, expected
        (331.516642392399, -97.1208394019004),  # true_solar_time_min_value, expected
    ],
)
def test_hour_angle_deg(true_solar_time_min_value, expected):
    result = noaa.hour_angle_deg(true_solar_time_min_value)
    almostequal(result, expected)


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
    almostequal(result, expected)


@pytest.mark.parametrize(
    "solar_zenith_angle_deg_value, expected",
    [
        (115.245718494866, -25.245718494866),  # solar_zenith_angle_deg_value, expected
        (95.2408647936783, -5.24086479367834),  # solar_zenith_angle_deg_value, expected
    ],
)
def test_solar_elevation_angle_deg(solar_zenith_angle_deg_value, expected):
    result = noaa.solar_elevation_angle_deg(solar_zenith_angle_deg_value)
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    almostequal(result, expected)


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
    "latitude, longitude, timezone, thedate, expected",
    [
        (
            40,
            -105,
            -6,
            datetime.datetime(2010, 6, 21, 0, 6),
            (-25.2334819743467, 345.86910228316),
        ),  # latitude, longitude, timezone, thedate, expected
        (
            37.4219444444444,
            -122.079583333333,
            -8,
            datetime.datetime(2023, 9, 21, 5, 33),
            (-5.17796026715717, 85.1264242410581),
        ),  # latitude, longitude, timezone, thedate, expected
    ],
)
def test_sunposition(latitude, longitude, timezone, thedate, expected):
    result_alt, result_azm = noaa.sunposition(latitude, longitude, timezone, thedate)
    expected_alt, expected_azm = expected
    almostequal(result_alt, expected_alt)
    almostequal(result_azm, expected_azm)


@pytest.mark.parametrize(
    "latitude, longitude, timezone, thedates, expected",
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
        ),  # latitude, longitude, timezone, thedates, expected
        (
            40,
            -105,
            -6,
            noaa.datetimerange(
                datetime.datetime(2010, 6, 21, 0, 6),
                datetime.datetime(2010, 6, 22, 0, 0),
                6,
            ),
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
        ),  # latitude, longitude, timezone, thedates, expected
        (
            37.4219444444444,
          -122.079583333333,
           -8,
            noaa.datetimerange(
                datetime.datetime(2023, 9, 21, 5, 33),
                datetime.datetime(2023, 9, 21, 5, 36),
                1,
            ),
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
        ),  # latitude, longitude, timezone, thedates, expected
    ],
)
def test_sunpositions(latitude, longitude, timezone, thedates, expected):
    result = noaa.sunpositions(latitude, longitude, timezone, thedates)
    for (r1, r2), (e1, e2) in zip(result, expected):
        almostequal(r1, e1)
        almostequal(r2, e2)
