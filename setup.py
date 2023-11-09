#!/usr/bin/env python

"""The setup script."""

import os

from setuptools import find_packages, setup

if os.path.exists('requirements.txt'):
    with open('requirements.txt') as f:
        install_requires = f.read().strip().split('\n')
else:
    install_requires = ['xmltodict', 'xsdata', 'xarray']

if os.path.exists('README.md'):
    with open('README.md') as f:
        long_description = f.read()
else:
    long_description = ''


setup(
    name='xncml',
    description='Tools for manipulating and opening NCML (NetCDF Markup) files with/for xarray',
    long_description=long_description,
    maintainer='Anderson Banihirwe',
    maintainer_email='abanihi@ucar.edu',
    url='https://github.com/xarray-contrib/xncml',
    packages=find_packages(),
    package_dir={'xncml': 'xncml'},
    include_package_data=True,
    install_requires=install_requires,
    license='Apache 2.0',
    zip_safe=False,
    keywords='xncml, xarray, netcdf',
    use_scm_version=True,
    python_requires='>=3.9, <4',
    setup_requires=['setuptools_scm', 'setuptools>=30.3.0', 'setuptools_scm_git_archive'],
    extras_require={
        'dev': ['pytest', 'flake8'],
    },
)
