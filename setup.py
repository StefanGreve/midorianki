#!/usr/bin/env python3

from typing import List, Optional

from setuptools import find_packages, setup

#region helper functions

def read_file(path: str, split: Optional[bool]=False) -> str | List[str]:
    with open(path, mode="r", encoding="utf-8") as file_handler:
        return file_handler.readlines() if split else file_handler.read()

#endregion

setup(
    author="Stefan Greve",
    author_email="greve.stefan@outlook.jp",
    name="midorianki",
    version="3.0.0",
    description="Tool for converting CSV files from Midori into APKG decks.",
    long_description=read_file("readme.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/StefanGreve/midorianki",
    project_urls={
        "Source Code": "https://github.com/StefanGreve/midorianki",
        "Bug Reports": "https://github.com/StefanGreve/midorianki/issues",
        "Changelog": "https://github.com/StefanGreve/midorianki/blob/master/CHANGELOG.md"
    },
    python_requires=">=3.11",
    install_requires=read_file("requirements/release.txt", split=True),
    extras_require={
        "dev": read_file("requirements/development.txt", split=True)[1:],
    },
    include_package_data=True,
    package_dir={
        "": "src"
    },
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "midorianki=midorianki.__main__:main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    keywords="cli, terminal, utils, anki",
)
