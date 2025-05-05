=========
Changelog
=========

`Unreleased <https://github.com/xarray-contrib/xncml/tree/master>`_ (latest)
----------------------------------------------------------------------------

Bug fixes
^^^^^^^^^

- Scalar attributes that are not strings are no longer wrapped in tuples of length==1 (by :user:`bzah`).

Breaking changes
^^^^^^^^^^^^^^^^

- Nested group handling (by :user:`bzah`):
    - Before this version, all groups were read, but conflicting variable names in-between groups would shadow data. Now, similarly to ``xarray.open_dataset``, ``open_ncml`` accepts an optional ``group`` argument to specify which group should be read. When ``group`` is not specified, it defaults to the root group. Additionally ``group`` can be set to ``'*'`` so that every group is read and the hierarchy is flattened. In the event of conflicting variable/dimension names across groups, the conflicting name will be modified by appending ``'__n'`` where n is incremented.
- Enums are no longer transformed into CF flag_values and flag_meanings attributes, instead they are stored in the ``encoding["dtype"].metadata`` of their respective variable. This is aligned with what was done on `xarray` v2024.01.0 (by :user:`bzah`).
- ``xncml.generated.ncml_2_2`` has been refactored to no longer be exposed to the package API. Users should now use objects imported directly from ``xncml.generated`` (by :user:`Zeitsperre`).
- Add support for Python 3.13 and drop support for Python 3.9 (by :user:`Zeitsperre`).

Internal changes
^^^^^^^^^^^^^^^^

- Added support for running `pytest` with `pytest-cov` (by :user:`Zeitsperre`).
- Reworked the GitHub CI testing workflow to perform version checks as well as tests with `pytest-cov` (by :user:`Zeitsperre`).
- The `xncml` package has been significantly restructured to improve maintainability (by :user:`bzah` and :user:`Zeitsperre`):
    - The package now complies with both PEP 517 and PEP 621 (``pyproject.toml`` and newer metadata definitions).
    - The build system has been migrated from `setuptools` to `flit`.
    - `CHANGES.rst` has been replaced with ``CHANGELOG.rst`` to follow the `keepachangelog` format.
    - Code linting and formatting now exclusively uses `ruff` (in lieu of `black`, `isort`, and others).
    - The package has adopted a ``src`` layout.
    - Documentation now uses `sphinx-apidoc` to generate API documentation on build and the module layout is now navigable on the documentation page.
    - The `xncml` package now uses `pytest` for testing, and the test suite has been migrated to `pytest` from `unittest`.
    - The project now uses Trusted Publisher to sign and verify releases.

.. _changes-0.4.0:

0.4.0 (2024-01-08)
------------------

- Add support for <EnumTypeDef> (by :user:`bzah`).
- Update XSD schema and dataclasses to latest version from netcdf-java to add support for unsigned types (by :user:`bzah`).
- Add support for scalar variables (by :user:`bzah`).
- [fix] empty attributes are now parsed into an empty string instead of crashing the parser (by :user:`bzah`).

.. _changes-0.3.1:

0.3.1 (2023-11-10)
------------------

- Add support for Python 3.12
- Drop support for Python 3.8


.. _changes-0.3:

0.3 (2023-08-28)
----------------

- Add `add_aggregation` and `add_variable_agg` to `Dataset` class (by :user:`huard`).
- Add `add_scan` to `Dataset` class (by :user:`huard`).
- Closing the dataset returned by `open_ncml` will close the underlying opened files (by :user:`huard`).
- Add `Dataset.from_text` classmethod  to create a `Dataset` from an XML string (by :user:`huard`).


.. _changes-0.2:

0.2 (2023-02-23)
----------------

- Implement `Dataset.rename_dataset_attribute` (by :user:`huard`).
- Allow empty `Dataset` creation (by :user:`huard`).
- Add support in `Dataset` for NcML documents using the `ncml` namespace (by :user:`huard`).
- Implement `Dataset.to_cf_dict` method to export CF-JSON dictionary (by :user:`huard`).


.. _changes-0.1:

0.1 Initial release (2022-11-24)
--------------------------------

 - Manipulate NcML file: add & remove attributes, variables and dimensions. (by :user:`andersy005`).
 - Implement `open_ncml`, which returns an `xarray.Dataset` built from an NcML. Note that
   Only a subset of the NcML syntax is supported. (by :user:`huard`).
