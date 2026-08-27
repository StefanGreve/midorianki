#!/usr/bin/env python3

import os
import platform
from pathlib import Path
from typing import Union

def get_resource_path(package_name: Union[str, Path]) -> Path:
    """
    Return a platform-specific resource directory for storing globally
    accessible package files.

    The directory is created if it does not already exist.

    Args:
        package_name: Name used as the leaf directory under the platform's
            per-user data location.

    Returns:
        The path to the (now existing) resource directory.
    """
    parent = None

    match platform.system():
        case "Windows":
            parent = Path(os.path.expandvars("%LOCALAPPDATA%"))
        case "Darwin":
            parent = Path.home() / "Library" / "Application Support"
        case _:
            # Assume Unix-like file system
            parent = Path.home() / ".config"

    resource_path = parent / package_name
    os.makedirs(resource_path, exist_ok=True)
    return resource_path
