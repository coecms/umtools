=============================
umtools
=============================

Miscellaneous tools for working with the Unified Model

.. image:: https://readthedocs.org/projects/umtools/badge/?version=latest
  :target: https://readthedocs.org/projects/umtools/?badge=latest
.. image:: https://travis-ci.org/coecms/umtools.svg?branch=master
  :target: https://travis-ci.org/coecms/umtools
.. image:: https://circleci.com/gh/coecms/umtools.svg?style=shield
  :target: https://circleci.com/gh/coecms/umtools
.. image:: http://codecov.io/github/coecms/umtools/coverage.svg?branch=master
  :target: http://codecov.io/github/coecms/umtools?branch=master
.. image:: https://landscape.io/github/coecms/umtools/master/landscape.svg?style=flat
  :target: https://landscape.io/github/coecms/umtools/master
.. image:: https://codeclimate.com/github/coecms/umtools/badges/gpa.svg
  :target: https://codeclimate.com/github/coecms/umtools
.. # image:: https://badge.fury.io/py/umtools.svg
  :target: https://pypi.python.org/pypi/umtools

.. content-marker-for-sphinx

-------
Install
-------

Conda install::

    conda install -c coecms umtools

Pip install (into a virtual environment)::

    pip install umtools

---
Use
---

* **iris2netcdf:** Convert a UM or GRIB file to CF-NetCDF format
* **slabancil:** Convert a hierachy slab ocean ancillary to netcdf and back
* **ancil2climatology:** Select a single year from an ancillary file and convert it to periodic

-------
Develop
-------

Development install::

    git checkout https://github.com/coecms/umtools
    cd umtools
    conda env create -f conda/dev-environment.yml
    source activate umtools-dev
    pip install -e '.[dev]'

The `dev-environment.yml` file is for speeding up installs and installing
packages unavailable on pypi, `requirements.txt` is the source of truth for
dependencies.

Run tests::

    py.test

Build documentation::

    python setup.py build_sphinx
    firefox docs/_build/index.html

