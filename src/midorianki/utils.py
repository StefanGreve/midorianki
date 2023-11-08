#!/usr/bin/env python3

import logging
import os
import platform
import sys
from logging import Logger
from pathlib import Path
from typing import Union

from colorama import Fore, Style

from .metadata import __package__

#region logging

def get_resource_path(package_name: Union[str, Path]) -> Path:
    """
    Return a platform-specific resource directory for storing globally
    accessible package files.
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

def shutdown(logger: Logger) -> None:
    """
    Perform any cleanup actions in the logging system (e.g. flushing buffers).

    Should be called at application exit.
    """
    for handler in reversed(logger.handlers):
        try:
            handler.acquire()
            handler.flush()
            handler.close()
        except (OSError, ValueError):
            # Ignore errors which might be caused by closed handlers that still
            # have references to them around at application exit
            pass
        finally:
            handler.release()

log_file_path = get_resource_path(__package__) / "error.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s::%(levelname)s::%(lineno)d::%(name)s::%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# monkey-patch for safe use
logger.shutdown = lambda: shutdown(logger)

#endregion logging

#region terminal formatting

def print_on_success(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted success message if verbose is enabled.
    """
    if not verbose: return
    print(f"{Style.BRIGHT}{Fore.GREEN}{'[  OK  ]'.ljust(12, ' ')}{Style.RESET_ALL}{message}", **kwargs)

def print_on_info(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted warning message if verbose is enabled.
    """
    if not verbose: return
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'[ INFO ]'.ljust(12, ' ')}{Style.RESET_ALL}{message}", **kwargs)

def print_on_warning(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted warning message if verbose is enabled.
    """
    if not verbose: return
    print(f"{Style.BRIGHT}{Fore.YELLOW}{'[ WARNING ]'.ljust(12, ' ')}{Style.RESET_ALL}{message}", **kwargs)

def print_on_error(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted error message if verbose is enabled.
    """
    if not verbose: return
    print(f"{Style.BRIGHT}{Fore.RED}{'[ ERROR ]'.ljust(12, ' ')}{Style.RESET_ALL}{message}", file=sys.stderr, **kwargs)

def clear():
    """
    Reset terminal screen.
    """
    os.system('cls' if platform.system() == 'Windows' else 'clear')

#endregion terminal formatting
