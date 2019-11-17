#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='PyConfigMaker',
      version='0.2',
      description='Generates a config and an argument parser from a yaml file',
      author='Claas Voelcker',
      author_email='claas@voelcker.net',
      packages=find_packages(),
      install_requires=['pyyaml']
     )

