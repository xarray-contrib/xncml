# xncml

![Read the Docs](https://img.shields.io/readthedocs/xncml)
![PyPI](https://img.shields.io/pypi/v/xncml)


Tools for opening and manipulating NcML (NetCDF Markup Language) files with/for xarray.

These tools allow you to modify NcML by:

- Adding or removing global attributes
- Adding or removing variable attributes
- Removing variables and dimensions

and read NcML files into `xarray.Dataset` objects:

```python
import xncml
ds = xncml.open_ncml("large_ensemble.ncml")
```

See [documentation] for more information.

## Installation

xncml can be installed from PyPI with pip:

```bash
pip install xncml
```

[documentation]: https://xncml.readthedocs.io
