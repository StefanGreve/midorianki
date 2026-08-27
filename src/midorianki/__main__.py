#!/usr/bin/env python3

"""Command-line entry point for the midorianki application."""

from .cli import build_parser
from .logger import init_logger
from .metadata import __package__, __version__
from .midorianki import export


def main() -> None:
    """Parse command-line arguments and run the requested command."""
    description = "Tool for converting CSV files from Midori into APKG decks."
    parser = build_parser(__package__, __version__, description)
    args = parser.parse_args()
    logger = init_logger(args.verbose)

    try:
        match args.command:
            case "convert":
                export(args.file, args.name, args.dest, args.verbose, logger)
            case _:
                # argparse prints the help manual and exits if there are any
                # errors on parsing, so there's no need to handle this case
                # here as it will accomplish nothing
                pass
    except Exception as error:
        logger.error(str(error))


if __name__ == "__main__":
    main()
