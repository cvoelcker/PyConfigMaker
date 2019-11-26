#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='PyConfigMaker',
      version='1.4',
      description='Generates a config and an argument parser from a yaml file',
      author='Claas Voelcker',
      author_email='claas@voelcker.net',
      packages=find_packages(),
      install_requires=['pyyaml'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/cvoelcker/PyConfigMaker',
      package_data={'config_parser': ['py.typed']},
      zip_safe=False
     )

