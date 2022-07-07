#!/usr/bin/env python
"""Top-level module for xncml."""
from pkg_resources import DistributionNotFound, get_distribution

from .core import Dataset
from .parser import open_ncml

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
finally:
    del get_distribution, DistributionNotFound
