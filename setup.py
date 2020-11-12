#!/usr/bin/env python
#
# Uses Python Build Reasonableness https://docs.openstack.org/developer/pbr/
# Add configuration to `setup.cfg`

from setuptools import setup, find_packages

setup(
    name="umtools",
    packages=find_packages("."),
    install_requires=[],
    entry_points={"console_scripts": ["umtool=umtools.umtool:main",]},
)
