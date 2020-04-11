#!/usr/bin/env python

from setuptools import setup

setup(
    author = "Stefan Greve",
    keywords = "japanese anki deck",
    name = 'midorianki',
    version = '0.1',
    description = "Script for converting CSV files from Midori to APKG.",
    url = "https://github.com/StefanGreve/midori-anki",
    py_modules = [ "midorianki" ],
    package_dir = { '' : 'src' },
    install_requires = [
        'click',
        'colorama',
        'genanki',
        'pathlib',
    ],

    python_requires=">=3.6.1",

    classifiers = [
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)
