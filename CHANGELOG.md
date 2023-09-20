0.4 (unreleased)
================

- Support parallel reads in `open_ncml` using `dask`. By @huard


0.3 (2023-08-28)
================

- Add `add_aggregation` and `add_variable_agg` to `Dataset` class. By @huard
- Add `add_scan` to `Dataset` class. By @huard
- Closing the dataset returned by `open_ncml` will close the underlying opened files. By @huard
- Add `Dataset.from_text` classmethod  to create a `Dataset` from an XML string. By @huard


0.2 (2023-02-23)
================

- Implement `Dataset.rename_dataset_attribute`. By @huard
- Allow empty `Dataset` creation. By @huard
- Add support in `Dataset` for NcML documents using the `ncml` namespace. By @huard
- Implement `Dataset.to_cf_dict` method to export CF-JSON dictionary. By @huard.


0.1 Initial release (2022-11-24)
================================

 - Manipulate NcML file: add & remove attributes, variables and dimensions. By @andersy005
 - Implement `open_ncml`, which returns an `xarray.Dataset` built from an NcML. Note that
   Only a subset of the NcML syntax is supported. By @huard
