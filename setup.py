# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in leaf/__init__.py
from leaf import __version__ as version

setup(
	name='leaf',
	version=version,
	description='Leaf',
	author='jan',
	author_email='jangeles@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
