#!/usr/bin/python

from setuptools import setup
from fortepy import __version__

setup(
    name="fortepy",
    version=__version__,
    author="Kevin Wang",
    author_email="kevmo314@gmail.com",
    maintainer="Kevin Wang",
    maintainer_email="kevmo314@gmail.com",
    url="https://github.com/kevmo314/FortePy",
    description="Python bindings for Forte Payments",
    install_requires=[
		'six'
    ],
    packages=[	
        'fortepy'
    ]
)
