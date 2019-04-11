===============================
xncml
===============================

.. image:: https://img.shields.io/circleci/project/github/NCAR/xncml/master.svg?style=for-the-badge&logo=circleci
    :target: https://circleci.com/gh/NCAR/xncml/tree/master

.. image:: https://img.shields.io/codecov/c/github/NCAR/xncml.svg?style=for-the-badge
    :target: https://codecov.io/gh/NCAR/xncml


.. image:: https://img.shields.io/readthedocs/xncml/latest.svg?style=for-the-badge
    :target: https://xncml.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/xncml.svg?style=for-the-badge
    :target: https://pypi.org/project/xncml
    :alt: Python Package Index


Tools for manipulating NcML (NetCDF Markup Language) files with/for xarray.

These tools allow you to modify NcML by:

- Adding or removing global attributes
- Adding or removing variable attributes
- Removing variables and dimensions


See documentation_ for more information.

.. _documentation: https://xncml.readthedocs.io


Installation
------------

xncml can be installed from PyPI with pip:

.. code-block:: bash

    pip install xncml
