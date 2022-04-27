# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='Health',
    version='0.1.0',
    description='Tool to collect health data',
    long_description=readme,
    author='Erich Reitz',
    author_email='erreitz@outlook.com',
    url='https://github.com/Erich-Reitz/Health',
    license='LICENSE.txt',
    packages=find_packages(exclude=('tests', 'docs'))
)

