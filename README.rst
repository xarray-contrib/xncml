xncml
=====

|pypi| |ruff| |docs|

Tools for opening and manipulating NcML (NetCDF Markup Language) files with/for xarray.

These tools allow you to modify NcML by:

- Adding or removing global attributes
- Adding or removing variable attributes
- Removing variables and dimensions

and read NcML files into `xarray.Dataset` objects:

.. code-block:: python

   import xncml
   ds = xncml.open_ncml("large_ensemble.ncml")


See `doc`_ for more information.


Installation
============

Stable release
--------------

To install xncml, run this command in your terminal:

.. code-block:: console

   python -m pip install xncml

This is the preferred method to install xncml, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for xncml can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

   git clone git@github.com:xarray-contrib/xncml/

Or download the `tarball`_:

.. code-block:: console

   curl -OJL https://github.com/xarray-contrib/xncml/tarball/main

Once you have a copy of the source, you can install it with:

.. code-block:: console

   python -m pip install .

.. _doc: https://readthedocs.org/projects/xncml
.. _Github repo: https://github.com/xarray-contrib/xncml/
.. _tarball: https://github.com/xarray-contrib/xncml/tarball/main

.. |docs| image:: https://readthedocs.org/projects/xncml/badge/?version=latest
        :target: hhttps://xncml.readthedocs.io
        :alt: Documentation Status

.. |pypi| image:: https://img.shields.io/pypi/v/xncml.svg
        :target: https://pypi.python.org/pypi/xncml
        :alt: Python Package Index Build

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
        :target: https://github.com/astral-sh/ruff
        :alt: Ruff
