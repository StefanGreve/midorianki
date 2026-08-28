#!/usr/bin/env python3

"""Command-line interface for the midorianki application."""

from pathlib import Path
from types import SimpleNamespace
from typing import Annotated

import typer

from .ankiconnect import import_deck
from .logger import init_logger
from .metadata import __package__, __version__
from .midorianki import export

app = typer.Typer(
    name=__package__,
    help="Tool for converting CSV files from Midori into APKG decks.",
    no_args_is_help=True,
    add_completion=True,
)


def _version_callback(value: bool) -> None:
    """
    Print the version and exit when ``--version`` is supplied.

    Args:
        value: ``True`` when the ``--version`` flag was passed.
    """
    if value:
        typer.echo(f"{__package__} {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    verbose: Annotated[bool, typer.Option("--verbose/--no-verbose", help="increase output verbosity")] = True,
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=_version_callback, is_eager=True, help="show the version and exit"),
    ] = None,
) -> None:
    """
    Configure shared state before dispatching to a command.

    The package-root logger is initialized here so that ``--verbose`` and
    ``--no-verbose`` behave as global flags that apply to every subcommand.

    Args:
        ctx: Invocation context carrying the shared logger and verbosity to the
            selected command.
        verbose: When ``True`` (the default), INFO and WARNING records reach the
            console; errors and the file log are unaffected.
        version: Handled eagerly by ``_version_callback``; unused here.
    """
    ctx.obj = SimpleNamespace(verbose=verbose, logger=init_logger(verbose))


@app.command(help="Convert CSV files into APKG decks.")
def convert(
    ctx: typer.Context,
    path: Annotated[Path, typer.Option("--path", metavar="PATH", help="path to CSV file")],
    dest: Annotated[
        Path | None, typer.Option("--dest", metavar="PATH", help="APKG target directory (default: current directory)")
    ] = None,
    name: Annotated[str | None, typer.Option("--name", help="deck filename and title (default: file stem)")] = None,
) -> None:
    """
    Convert CSV files into APKG decks.

    Args:
        ctx: Invocation context providing the shared logger and verbosity.
        path: Path to the source CSV file.
        dest: Directory in which the ``.apkg`` file is written; defaults to the
            current working directory.
        name: Deck filename and title; defaults to the CSV file stem.
    """
    try:
        export(path, name, dest or Path.cwd(), ctx.obj.verbose, ctx.obj.logger)
    except Exception as error:
        # route failures through the logger so they reach both stderr and the
        # file log, then exit non-zero instead of raising a Typer traceback
        ctx.obj.logger.error(str(error))
        raise typer.Exit(code=1) from error


@app.command(name="import", help="Import an APKG deck into a running Anki via AnkiConnect.")
def import_(
    ctx: typer.Context,
    path: Annotated[Path, typer.Option("--path", metavar="PATH", help="path to APKG deck")],
    host: Annotated[str, typer.Option("--host", help="AnkiConnect host")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", help="AnkiConnect port")] = 8765,
) -> None:
    """
    Import an APKG deck into a running Anki via AnkiConnect.

    Args:
        ctx: Invocation context providing the shared logger and verbosity.
        path: Path to the ``.apkg`` deck to import.
        host: AnkiConnect host; defaults to ``127.0.0.1``.
        port: AnkiConnect port; defaults to ``8765``.
    """
    try:
        import_deck(path, host=host, port=port, logger=ctx.obj.logger)
    except Exception as error:
        # mirror convert: log the failure (stderr + file log) and exit non-zero
        ctx.obj.logger.error(str(error))
        raise typer.Exit(code=1) from error
