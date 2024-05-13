Changelog
=========

`Unreleased <https://github.com/xarray-contrib/xncml/tree/master>`_ (latest)
----------------------------------------------------------------------------

- Added support for running `pytest` with `pytest-cov`. By @Zeitsperre
- Reworked the GitHub CI testing workflow to perform version checks as well as tests with `pytest-cov` . By @Zeitsperre

Breaking changes
^^^^^^^^^^^^^^^^

- Nested group handling:
  Before this version, all groups were read, but conflicting variable names in-between groups would shadow data.  Now, similarly to xarray ``open_dataset``, ``open_ncml`` accepts an optional ``group`` argument to specify which group should be read. When ``group`` is not specified, it defaults to the root group. Additionally ``group`` can be set to ``'*'`` so that every group is read and the hierarchy is flattened.   In the event of conflicting variable/dimension names across groups, the conflicting name will be modified by appending ``'__n'`` where n is incremented.
- Enums are no longer transformed into CF flag_values and flag_meanings attributes, instead they are stored in the ``encoding["dtype"].metadata`` of their respective variable. This is aligned with what is done on xarray v2024.01.0
- [fix] scalar attributes that are not strings are no longer wrapped in tuples of length 1.

.. _changes-0.4.0:

0.4.0 (2024-01-08)
------------------

- Add support for <EnumTypeDef>. By @bzah
- Update XSD schema and dataclasses to latest version from netcdf-java to add support for unsigned types. By @bzah
- Add support for scalar variables. By @Bzah
- [fix] empty attributes are now parsed into an empty string instead of crashing the parser.  By @Bzah

.. _changes-0.3.1:

0.3.1 (2023-11-10)
------------------

- Add support for Python 3.12
- Drop support for Python 3.8


.. _changes-0.3:

0.3 (2023-08-28)
----------------

- Add `add_aggregation` and `add_variable_agg` to `Dataset` class. By @huard
- Add `add_scan` to `Dataset` class. By @huard
- Closing the dataset returned by `open_ncml` will close the underlying opened files. By @huard
- Add `Dataset.from_text` classmethod  to create a `Dataset` from an XML string. By @huard


.. _changes-0.2:

0.2 (2023-02-23)
----------------

- Implement `Dataset.rename_dataset_attribute`. By @huard
- Allow empty `Dataset` creation. By @huard
- Add support in `Dataset` for NcML documents using the `ncml` namespace. By @huard
- Implement `Dataset.to_cf_dict` method to export CF-JSON dictionary. By @huard.


.. _changes-0.1:

0.1 Initial release (2022-11-24)
--------------------------------

 - Manipulate NcML file: add & remove attributes, variables and dimensions. By @andersy005
 - Implement `open_ncml`, which returns an `xarray.Dataset` built from an NcML. Note that
   Only a subset of the NcML syntax is supported. By @huard
