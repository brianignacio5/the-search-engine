#!/usr/bin/env python
from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = []

setup(
    name='tsg',
    version=0.01,
    #  url='',
    author='Moritz, Miguel and Brian',
    author_email='mail@moritzs.de',
    description=('A cool search engine and \
                 crawler for http://dblp.uni-trier.de/'),
    license='',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    scripts=[],
    install_requires=['requests', 'nose', 'lxml', 'mock']
)
