# xncml

#.. image:: <https://img.shields.io/codecov/c/github/xarray-contrib/xncml.svg?style=for-the-badge>
\#    :target: <https://codecov.io/gh/xarray-contrib/xncml>

```{image} https://img.shields.io/readthedocs/xncml/latest.svg?style=for-the-badge
:alt: Documentation Status
:target: https://xncml.readthedocs.io/en/latest/?badge=latest
```

```{image} https://img.shields.io/pypi/v/xncml.svg?style=for-the-badge
:alt: Python Package Index
:target: https://pypi.org/project/xncml
```

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
