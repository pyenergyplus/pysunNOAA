pysunNOAA
=========

Python implementation of NOAA's Solar Position Calculators


`NOAA <https://www.noaa.gov>`_ has the calculation details at their website at `Solar Calculation Details <source ~/venvs/pysunnoaa/bin/activate>`_ 

**pysunNOAA** is based on the spreadsheet `NOAA_Solar_Calculations_day.xls <https://www.gml.noaa.gov/grad/solcalc/NOAA_Solar_Calculations_day.xls>`_ . All the calculation cells in row 2 of the spreadsheet are implemented in pysunNOAA. This is a work in progress. But it is fully usable at this point

Here is what it can do::

    import datetime
    from pysunnoaa import noaa

    latitude = 40 # Latitude (+ to N)
    longitude = -105 # Longitude (+ to E)
    timezone = -6 # Time Zone (+ to E)
    thedatetime = datetime.datetime(2010, 6, 21, 9, 54)

    altitude, azimuth = noaa.sunposition(
    latitude, longitude, timezone, thedatetime, atm_corr=True
    )

    print(f"{altitude=}, {azimuth=}")

    >> altitude=47.36178497432497, azimuth=98.30691558695895

The above calculation is corrected for atmospheric diffraction. We can also do the calculation without the correction for atmospheric diffraction by setting ``atm_corr=False``::

    altitude, azimuth = noaa.sunposition(
        latitude, longitude, timezone, thedatetime, atm_corr=False
    )
    print(f"{altitude=}, {azimuth=}")
    
    >> altitude=47.346932081680364, azimuth=98.30691558695895

Let us take a look at generating multiple sun positions for a time series. First we have to generate the time series::

    thedates = noaa.datetimerange(
        datetime.datetime(2024, 6, 21, 10), # start
        datetime.datetime(2024, 6, 21, 11), # stop
        minutes=10 # step
    ) # The arguments are similar to python's range. 
      # It returns a generator
    for thedate in thedates:
        print(thedate)

    2024-06-21 10:00:00
    2024-06-21 10:10:00
    2024-06-21 10:20:00
    2024-06-21 10:30:00
    2024-06-21 10:40:00
    2024-06-21 10:50:00

So let us generate the sun positions for this time series::

    thedates = noaa.datetimerange(
        datetime.datetime(2024, 6, 21, 10),
        datetime.datetime(2024, 6, 21, 11),
        minutes=10
    )

    positions = noaa.sunpositions(latitude, longitude, timezone, thedates, atm_corr=False)
    for altitude, azimuth in positions:
        print(f"{altitude=}, {azimuth=}")

    altitude=48.44972994443188, azimuth=99.43756106034147
    altitude=50.33276597510335, azimuth=101.44934328356527
    altitude=52.20206053830976, azimuth=103.57347468902549
    altitude=54.05415607848319, azimuth=105.82830623146941
    altitude=55.88497413825557, azimuth=108.23537482765607
    altitude=57.689656999063025, azimuth=110.82001062044083

Let us print this again::

    for altitude, azimuth in positions:
        print(f"{altitude=}, {azimuth=}")

WHAT !!! Why did it not print anything ??

Both ``noaa.datetimerange`` and ``noaa.sunpositions`` are generators. Once you loop through the generator, the values are exhausted (or emptied). To get the values again you will need to call the functions again::


    thedates = noaa.datetimerange(
        datetime.datetime(2024, 6, 21, 10),
        datetime.datetime(2024, 6, 21, 11),
        minutes=10
    )

    positions = noaa.sunpositions(latitude, longitude, timezone, thedates, atm_corr=False)
    for altitude, azimuth in positions:
        print(f"{altitude=}, {azimuth=}")

    altitude=48.44972994443188, azimuth=99.43756106034147
    altitude=50.33276597510335, azimuth=101.44934328356527
    altitude=52.20206053830976, azimuth=103.57347468902549
    altitude=54.05415607848319, azimuth=105.82830623146941
    altitude=55.88497413825557, azimuth=108.23537482765607
    altitude=57.689656999063025, azimuth=110.82001062044083

That's all for now.
