#!/usr/bin/env python3

import logging
from logging import Logger

from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text

from .metadata import __package__
from .utils import get_resource_path

logging.addLevelName(logging.DEBUG, "DBG")
logging.addLevelName(logging.INFO, "INF")
logging.addLevelName(logging.WARNING, "WRN")
logging.addLevelName(logging.ERROR, "ERR")
logging.addLevelName(logging.CRITICAL, "FTL")

_LEVEL_STYLES = {
    logging.DEBUG: "logging.level.debug",
    logging.INFO: "logging.level.info",
    logging.WARNING: "logging.level.warning",
    logging.ERROR: "logging.level.error",
    logging.CRITICAL: "logging.level.critical",
}

_BRACKET_STYLE = "grey50"

class BracketRichHandler(RichHandler):
    """
    RichHandler that renders the level name wrapped in muted brackets while
    keeping the name itself color-highlighted, e.g. ``[ INF ]``.
    """
    def get_level_text(self, record: logging.LogRecord) -> Text:
        style = _LEVEL_STYLES.get(record.levelno, "logging.level.info")
        return Text.assemble(("[ ", _BRACKET_STYLE), (record.levelname, style), (" ]", _BRACKET_STYLE))

def init_logger(enable_console_logger: bool) -> Logger:
    """
    Configure and return the package-root logger.

    A file handler that writes detailed records to ``error.log`` and an error
    handler that reports errors to stderr are always attached. Handlers are
    attached to the package-root logger so that records from any submodule
    (``getLogger(__name__)``) propagate up to them.

    Args:
        enable_console_logger: When ``True``, also emit INFO and WARNING records
            to stdout via rich. Errors and the file log are unaffected by this
            flag.

    Returns:
        The configured package-root logger.
    """
    logger = logging.getLogger(__package__)
    logger.setLevel(logging.INFO)

    if logger.handlers: return logger

    log_file_path = get_resource_path(__package__) / "error.log"
    _file_handler = logging.FileHandler(log_file_path)
    _file_handler.setFormatter(logging.Formatter('%(asctime)s::%(levelname)s::%(lineno)d::%(name)s::%(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(_file_handler)

    error_console = Console(stderr=True)
    _error_handler = BracketRichHandler(console=error_console, level=logging.ERROR, show_time=False, show_path=False)
    _error_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(_error_handler)

    if enable_console_logger:
        console = Console()
        _console_handler = BracketRichHandler(console=console, show_time=False, show_path=False)
        _console_handler.setFormatter(logging.Formatter("%(message)s"))
        _console_handler.addFilter(lambda record: record.levelno < logging.ERROR)
        logger.addHandler(_console_handler)

    return logger
