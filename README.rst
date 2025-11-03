xncml
=====

+----------------------------+-----------------------------------------------------+
| Versions                   | |pypi|                                              |
+----------------------------+-----------------------------------------------------+
| Documentation and Support  | |docs| |versions|                                   |
+----------------------------+-----------------------------------------------------+
| Open Source                | |license|                                           |
+----------------------------+-----------------------------------------------------+
| Coding Standards           | |ruff| |pre-commit|                                 |
+----------------------------+-----------------------------------------------------+
| Development Status         | |status| |build| |coveralls|                        |
+----------------------------+-----------------------------------------------------+

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

.. |build| image:: https://github.com/xarray-contrib/xncml/actions/workflows/main.yml/badge.svg
        :target: https://github.com/xarray-contrib/xncml/actions/workflows/main.yml
        :alt: Build Status

.. |coveralls| image:: https://coveralls.io/repos/github/xarray-contrib/xncml/badge.svg
        :target: https://coveralls.io/github/xarray-contrib/xncml
        :alt: Coveralls

.. |docs| image:: https://readthedocs.org/projects/xncml/badge/?version=latest
        :target: https://xncml.readthedocs.io
        :alt: Documentation Status

.. |license| image:: https://img.shields.io/github/license/xarray-contrib/xncml.svg
        :target: https://github.com/xarray-contrib/xncml/blob/main/LICENSE
        :alt: License

..
    .. |ossf-bp| image:: https://bestpractices.coreinfrastructure.org/projects/????/badge
            :target: https://bestpractices.coreinfrastructure.org/projects/????
            :alt: Open Source Security Foundation Best Practices

    .. |ossf-score| image:: https://api.securityscorecards.dev/projects/github.com/xarray-contrib/xncml/badge
            :target: https://securityscorecards.dev/viewer/?uri=github.com/xarray-contrib/xncml
            :alt: OpenSSF Scorecard

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/xarray-contrib/xncml/main.svg
        :target: https://results.pre-commit.ci/latest/github/xarray-contrib/xncml/main
        :alt: pre-commit.ci status

.. |pypi| image:: https://img.shields.io/pypi/v/xncml.svg
        :target: https://pypi.python.org/pypi/xncml
        :alt: Python Package Index Build

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
        :target: https://github.com/astral-sh/ruff
        :alt: Ruff

.. |status| image:: https://www.repostatus.org/badges/latest/active.svg
        :target: https://www.repostatus.org/#active
        :alt: Project Status: Active – The project has reached a stable, usable state and is being actively developed.

.. |versions| image:: https://img.shields.io/pypi/pyversions/xncml.svg
        :target: https://pypi.python.org/pypi/xncml
        :alt: Supported Python Versions
