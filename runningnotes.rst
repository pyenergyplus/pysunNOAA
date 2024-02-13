2024-02-13
==========

- finihed coding all the cells
- do the function that just gives azimuth and alt

2024-02-04
==========

Giving up on poetry for now.

- using https://pypi.org/project/julian/ for julian day
- matches test against https://aa.usno.navy.mil/data/JulianDate

- 28 total functions
- completed 16 on 2024-02-06
- 12 to go

2024-02-01
==========

Strategy:

- install poetry on this computer using install-script
    - TODO docuemnt steps here

::

    # curl -sSL https://install.python-poetry.org | python3 -
    python3 -m pip install pipx
    python3  -m pipx install poetry

    # other functions:
    python3 -m pipx upgrade poetry
    python3 -m pipx uninstall poetry

- create pyproject.toml on pysunnoaa
    - TODO document how

::

    
- move data from requirements.txt and requrements_dev.txt
    - TODO document how
- install pyproject.toml data into virtualenv
    - TODO document how
- also test a pip install of the whole package
    - does it work without setup.py

hmmmm. how do you know this worked?

- have simple data in requirements.txt and requirements_dev.txt
    - requirements.txt
        - epconversions
    - requirements_dev.txt
        - tinynumpy
- make virtual env trypoetry
    - alter use poetry to make the file
-  
