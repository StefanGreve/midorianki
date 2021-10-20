#!/usr/bin/env python3

import logging
import os
import platform
import sys
from pathlib import Path
from typing import Union

from . import config
from .__init__ import package_name
from .config import BRIGHT, GREEN, RED, RESET_ALL, YELLOW

#region logging

def get_config_dir() -> Path:
    """
    Return a platform-specific root directory for user configuration settings.
    """
    return {
        'Windows': Path(os.path.expandvars('%LOCALAPPDATA%')),
        'Darwin': Path.home().joinpath('Library').joinpath('Application Support'),
        'Linux': Path.home().joinpath('.config')
    }[platform.system()].joinpath(package_name)

def get_resource_path(filename: Union[str, Path]) -> Path:
    """
    Return a platform-specific log file path.
    """
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    resource = config_dir.joinpath(filename)
    resource.touch(exist_ok=True)
    return resource

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(lineno)d::%(name)s::%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(get_resource_path(config.LOGFILE))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def reset_file(filename: Union[str, Path]) -> None:
    open(get_resource_path(filename), mode='w', encoding='utf-8').close()

#endregion logging

#region terminal formatting

def print_on_success(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted success message if verbose is enabled.
    """
    if verbose:
        print(f"{BRIGHT}{GREEN}{'[  OK  ]'.ljust(12, ' ')}{RESET_ALL}{message}", **kwargs)

def print_on_info(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted warning message if verbose is enabled.
    """
    if verbose:
        print(f"{BRIGHT}{YELLOW}{'[ INFO ]'.ljust(12, ' ')}{RESET_ALL}{message}", **kwargs)

def print_on_warning(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted warning message if verbose is enabled.
    """
    if verbose:
        print(f"{BRIGHT}{YELLOW}{'[ WARNING ]'.ljust(12, ' ')}{RESET_ALL}{message}", **kwargs)

def print_on_error(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted error message if verbose is enabled.
    """
    if verbose:
        print(f"{BRIGHT}{RED}{'[ ERROR ]'.ljust(12, ' ')}{RESET_ALL}{message}", file=sys.stderr, **kwargs)

def clear():
    """
    Reset terminal screen.
    """
    os.system('cls' if platform.system() == 'Windows' else 'clear')

#endregion terminal formatting
