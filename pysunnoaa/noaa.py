"""All the functions to calculate the sun postion using the NOAA spreadsheet"""

import datetime
import math
import julian

def add2(a):
    return a + 2 

def julianday(dt, timezone=0):
    """return the julain day for the datetime"""
    dt_tz = dt - datetime.timedelta(hours=timezone)
    return julian.to_jd(dt_tz)

def juliancentury(jul_day):
    """g2"""
    return (jul_day-2451545)/36525

def geom_mean_long_sun_deg(jul_century):
    """i2"""
    return (280.46646 + jul_century * (36000.76983 + jul_century * 0.0003032)) % 360

def geom_mean_anom_sun_deg(jul_century):
    """j2"""
    return 357.52911 + jul_century * (35999.05029 - 0.0001537 * jul_century)
    
def eccent_earth_orbit(jul_century):
    """k2"""
    return 0.016708634 - jul_century * (0.000042037 + 0.0000001267 * jul_century)

def sun_eq_of_ctr(jul_century, geom_mean_anom_sun_value):
    """l2"""
    g2 = jul_century 
    j2 = geom_mean_anom_sun_value
    return math.sin(math.radians(j2)) * (1.914602- g2 * (0.004817 + 0.000014 * g2)) + math.sin(math.radians(2 * j2)) * (0.019993 - 0.000101 * g2) + math.sin(math.radians(3 * j2)) * 0.000289

func_f2 = julianday #1
func_g2 = juliancentury #2
func_i2 = geom_mean_long_sun_deg #3
func_j2 = geom_mean_anom_sun_deg #4
func_k2 = eccent_earth_orbit #5
func_l2 = sun_eq_of_ctr #6

def main():
    latitude = b3 = 40
    longitude = b4 = -105
    time_zone = b5 = -6
    date = b7 = d2 = datetime.datetime(2010, 6, 21, 0, 6)
    # e2 = 0.1/24
    f2 = func_f2(date, time_zone)
    g2 = func_g2(f2)
    i2 = func_i2(g2)
    j2 = func_j2(g2)
    k2 = func_k2(g2)
    l2 = func_l2(g2, j2)
    print(f"{f2=}")
    print(f"{g2=}")
    print(f"{i2=}")
    print(f"{j2=}")
    print(f"{k2=}")
    print(f"{l2=}")

if __name__ == '__main__':
    main()
