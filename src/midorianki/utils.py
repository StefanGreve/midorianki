#!/usr/bin/env python3

import logging
import os
import platform
from logging import Logger
from pathlib import Path
from typing import Union

from rich.console import Console
from rich.text import Text
from rich.theme import Theme

from .metadata import __package__

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

#region terminal formatting

_theme = Theme({
    "success": "bold green",
    "info": "bold yellow",
    "warning": "bold yellow",
    "error": "bold red",
    "path": "cyan",
})

console = Console(theme=_theme)
error_console = Console(stderr=True, theme=_theme)

def _print_status(target: Console, label: str, style: str, message: str, verbose: bool, **kwargs) -> None:
    if not verbose:
        return

    # The label is a literal Text so its own brackets never parse as markup; the
    # message is passed as a plain string, so callers can embed rich markup
    # (e.g. "[bold yellow]path[/]"). Pass markup=False (or rich.markup.escape the
    # message) when it may contain raw brackets from data such as file paths.
    label_text = Text(label.ljust(12), style=style)
    kwargs.setdefault("highlight", False)
    target.print(label_text, str(message), sep="", **kwargs)

def print_on_success(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted success message if verbose is enabled.
    """
    _print_status(console, "[  OK  ]", "success", message, verbose, **kwargs)

def print_on_info(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted info message if verbose is enabled.
    """
    _print_status(console, "[ INFO ]", "info", message, verbose, **kwargs)

def print_on_warning(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted warning message if verbose is enabled.
    """
    _print_status(console, "[ WARNING ]", "warning", message, verbose, **kwargs)

def print_on_error(message: str, verbose: bool=True, **kwargs) -> None:
    """
    Print a formatted error message to stderr if verbose is enabled.
    """
    # Exception text is arbitrary data: a stray "[/]" or malformed tag would
    # otherwise raise rich.errors.MarkupError from inside a caller's except block.
    kwargs.setdefault("markup", False)
    _print_status(error_console, "[ ERROR ]", "error", message, verbose, **kwargs)

def clear() -> None:
    """
    Reset terminal screen.
    """
    console.clear()

#endregion terminal formatting
