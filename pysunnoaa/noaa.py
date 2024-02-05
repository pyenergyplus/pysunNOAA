"""All the functions to calculate the sun postion using the NOAA spreadsheet"""

import datetime
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

def Geom_Mean_Long_Sun_deg(jul_century):
    """i2"""
    return (280.46646 + jul_century * (36000.76983 + jul_century * 0.0003032)) % 360

def Geom_Mean_Anom_Sun_deg():
    """"""
    pass
    
func_f2 = julianday
func_g2 = juliancentury
func_i2 = Geom_Mean_Long_Sun_deg

def main():
    latitude = b3 = 40
    longitude = b4 = -105
    time_zone = b5 = -6
    date = b7 = d2 = datetime.datetime(2010, 6, 21, 0, 6)
    # e2 = 0.1/24
    f2 = func_f2(date, time_zone)
    g2 = func_g2(f2)
    i2 = func_i2(g2)
    print(f"{f2=}")
    print(f"{g2=}")
    print(f"{i2=}")
    print(f"{g2=}")

if __name__ == '__main__':
    main()
