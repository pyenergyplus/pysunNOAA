"""All the functions to calculate the sun postion using the NOAA spreadsheet"""

import datetime
import math
import julian

def add2(a):
    return a + 2 

def julianday(dt, timezone=0):
    """return the julain day for the datetime

    1. f2"""
    dt_tz = dt - datetime.timedelta(hours=timezone)
    return julian.to_jd(dt_tz)

def juliancentury(jul_day):
    """2. g2"""
    return (jul_day-2451545)/36525

def geom_mean_long_sun_deg(jul_century):
    """3. i2"""
    return (280.46646 + jul_century * (36000.76983 + jul_century * 0.0003032)) % 360

def geom_mean_anom_sun_deg(jul_century):
    """4. j2"""
    return 357.52911 + jul_century * (35999.05029 - 0.0001537 * jul_century)
    
def eccent_earth_orbit(jul_century):
    """5. k2"""
    return 0.016708634 - jul_century * (0.000042037 + 0.0000001267 * jul_century)

def sun_eq_of_ctr(jul_century, geom_mean_anom_sun_value):
    """6. l2"""
    g2 = jul_century 
    j2 = geom_mean_anom_sun_value
    return math.sin(math.radians(j2)) * (1.914602- g2 * (0.004817 + 0.000014 * g2)) + math.sin(math.radians(2 * j2)) * (0.019993 - 0.000101 * g2) + math.sin(math.radians(3 * j2)) * 0.000289

def sun_true_long_deg(geom_mean_long_sun_deg_value, sun_eq_of_ctr_value):
    """7. m2"""
    i2 = geom_mean_long_sun_deg_value
    l2 = sun_eq_of_ctr_value
    return i2+l2

def sun_true_anom_deg(geom_mean_anom_sun_deg_value, sun_eq_of_ctr_value):
    """8. n2"""
    j2 = geom_mean_anom_sun_deg_value
    l2 = sun_eq_of_ctr_value
    return j2+l2

def sun_rad_vector_AUs(eccent_earth_orbit_value, sun_true_anom_deg_value):
    """9. o2"""
    k2 = eccent_earth_orbit_value
    n2 = sun_true_anom_deg_value 
    return (1.000001018 * (1 - k2 * k2)) / (1 + k2 * math.cos(math.radians(n2)))

def sun_app_long_deg(juliancentury_value, sun_true_long_deg_value):
    """10. p2"""
    g2 = juliancentury_value
    m2 = sun_true_long_deg_value
    return m2 - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * g2))

def mean_obliq_ecliptic_deg(juliancentury_value):
    """11. q2"""
    g2 = juliancentury_value
    return 23 + (26 + ((21.448 - g2 * (46.815 + g2 * (0.00059 - g2 * 0.001813)))) / 60) /  60

def obliq_corr_deg(juliancentury_value, mean_obliq_ecliptic_deg_value):
    """12. r2"""
    g2 = juliancentury_value
    q2 = mean_obliq_ecliptic_deg_value
    return q2 + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * g2))

def sun_rt_ascen_deg(sun_app_long_deg_value, obliq_corr_deg_value):
    """13. s2"""
    p2 = sun_app_long_deg_value 
    r2 = obliq_corr_deg_value
    y = math.cos(math.radians(r2)) * math.sin(math.radians(p2))
    x = math.cos(math.radians(p2))
    return math.degrees(math.atan2(y, x))

def sun_declin_deg(sun_app_long_deg_value, obliq_corr_deg_value):
    """14. t2"""
    p2 = sun_app_long_deg_value 
    r2 = obliq_corr_deg_value 
    return math.degrees(math.asin(math.sin(math.radians(r2)) * math.sin(math.radians(p2))))

def var_y(obliq_corr_deg_value):
    """15. u2"""
    r2 = obliq_corr_deg_value
    return math.tan(math.radians(r2 / 2)) * math.tan(math.radians(r2 / 2))

def eq_of_time_minutes(geom_mean_long_sun_deg_value, geom_mean_anom_sun_deg_value, eccent_earth_orbit_value, var_y_value):
    """16. v2"""
    i2 = geom_mean_long_sun_deg_value
    j2 = geom_mean_anom_sun_deg_value
    k2 = eccent_earth_orbit_value
    u2 = var_y_value
    return 4 * math.degrees(u2 * math.sin(2 * math.radians(i2)) - 2 * k2 * math.sin(math.radians(j2)) + 4 *  k2 * u2 * math.sin(math.radians(j2)) * math.cos(2 * math.radians(i2)) - 0.5 * u2 * u2 * math.     sin(4 * math.radians(i2)) - 1.25 * k2 * k2 * math.sin(2 * math.radians(j2)))


func_f2 = julianday #1
func_g2 = juliancentury #2
func_i2 = geom_mean_long_sun_deg #3
func_j2 = geom_mean_anom_sun_deg #4
func_k2 = eccent_earth_orbit #5
func_l2 = sun_eq_of_ctr #6
func_m2 = sun_true_long_deg #7
func_n2 = sun_true_anom_deg #8
func_o2 = sun_rad_vector_AUs #9
func_p2 = sun_app_long_deg #10
func_q2 = mean_obliq_ecliptic_deg #11
func_r2 = obliq_corr_deg #12
func_s2 = sun_rt_ascen_deg #13
func_t2 = sun_declin_deg #14
func_u2 = var_y #15
func_v2 = eq_of_time_minutes #16

def main():
    latitude = b3 = 40
    longitude = b4 = -105
    time_zone = b5 = -6
    date = b7 = d2 = datetime.datetime(2010, 6, 21, 0, 6)
    e2 = date
    f2 = func_f2(e2, time_zone)
    g2 = func_g2(f2)
    i2 = func_i2(g2)
    # h2 -> nothin in cell
    j2 = func_j2(g2)
    k2 = func_k2(g2)
    l2 = func_l2(g2, j2)
    m2 = func_m2(i2, l2)
    n2 = func_n2(j2, l2)
    o2 = func_o2(k2, n2)
    p2 = func_p2(g2, m2)
    q2 = func_q2(g2)
    r2 = func_r2(g2, q2)
    s2 = func_s2(p2, r2)
    t2 = func_t2(p2, r2)
    u2 = func_u2(r2)
    v2 = func_v2(i2, j2, k2, u2)

    print(f"{f2=}")
    print(f"{g2=}")
    print(f"{i2=}")
    print(f"{j2=}")
    print(f"{k2=}")
    print(f"{l2=}")
    print(f"{m2=}")
    print(f"{n2=}")
    print(f"{o2=}")
    print(f"{p2=}")
    print(f"{q2=}")
    print(f"{r2=}")
    print(f"{s2=}")
    print(f"{t2=}")
    print(f"{u2=}")
    print(f"{v2=}")

if __name__ == '__main__':
    main()
