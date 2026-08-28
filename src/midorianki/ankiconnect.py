#!/usr/bin/env python3

"""AnkiConnect client for importing APKG decks into a running Anki instance."""

import json
import logging
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

_LOGGER = logging.getLogger(__name__)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
API_VERSION = 6

_ADDON_HINT = "Is Anki running with the AnkiConnect add-on (code 2055492159) installed?"


class AnkiConnectError(RuntimeError):
    """Raised when AnkiConnect is unreachable or reports an error for an action."""


def _invoke(action: str, host: str, port: int, timeout: float, **params: object) -> object:
    payload = json.dumps({"action": action, "version": API_VERSION, "params": params}).encode("utf-8")
    request = Request(f"http://{host}:{port}", data=payload, headers={"Content-Type": "application/json"})

    try:
        with urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except URLError as error:
        # covers connection-refused (Anki down) and socket timeouts, both of which
        # surface through URLError; HTTPError is a URLError subclass and lands here too
        raise AnkiConnectError(f"Cannot reach AnkiConnect on {host}:{port}. {_ADDON_HINT}") from error

    # AnkiConnect always returns both keys; a non-null error means the action failed
    if body.get("error") is not None:
        raise AnkiConnectError(str(body["error"]))

    return body["result"]


def import_deck(
    file: str | Path,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    timeout: float = 10.0,
    logger: logging.Logger = _LOGGER,
) -> bool:
    """
    Import an existing APKG deck into a running Anki via AnkiConnect.

    Requires Anki to be running with the AnkiConnect add-on (code ``2055492159``)
    listening on ``host:port``. The deck name is taken from the ``.apkg`` itself;
    AnkiConnect exposes no reliable rename action, so use ``convert --name`` to
    choose a name before importing.

    Args:
        file: Path to the ``.apkg`` deck to import.
        host: AnkiConnect host; defaults to ``127.0.0.1``.
        port: AnkiConnect port; defaults to ``8765``.
        timeout: Per-request socket timeout in seconds.
        logger: Logger used to report progress; defaults to this module's logger,
            whose records propagate to the configured package logger.

    Returns:
        ``True`` when AnkiConnect reports a successful import.

    Raises:
        AnkiConnectError: When the file is missing, AnkiConnect is unreachable, or
            the import is rejected.
    """
    path = Path(file)

    if not path.is_file():
        raise AnkiConnectError(f"File not found: {path}")

    # handshake first so an unreachable Anki fails with a clear message
    version = _invoke("version", host, port, timeout)
    logger.info(f"Connected to AnkiConnect (API v{version}) on {host}:{port}.")

    # importPackage documents its path as relative to collection.media, but the
    # underlying importer accepts an absolute path, so resolve to one
    imported = _invoke("importPackage", host, port, timeout, path=str(path.resolve()))

    if not imported:
        raise AnkiConnectError(f"AnkiConnect rejected the package {path.name!r}.")

    logger.info(f"Imported {path.name!r} into the local Anki collection.")

    return bool(imported)
