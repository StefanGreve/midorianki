#!/usr/bin/env python3

"""Package metadata sourced from the installed distribution."""

from importlib.metadata import metadata

__meta_data = metadata("midorianki")
__package__ = __meta_data["Name"]
__version__ = __meta_data["Version"]
