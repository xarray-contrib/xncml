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
