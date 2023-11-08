#!/usr/bin/env python3

from colorama import deinit, just_fix_windows_console

from .cli import build_parser
from .metadata import __package__, __version__
from .midorianki import export
from .utils import logger, print_on_error


def main() -> None:
    # Enable Windows' built-in ANSI support
    just_fix_windows_console()

    description = "Tool for converting CSV files from Midori into APKG decks."
    parser = build_parser(__package__, __version__, description)
    args = parser.parse_args()

    try:
        match args.command:
            case "convert":
                export(args.file, args.name, args.dest, args.verbose)
            case _:
                # argparse prints the help manual and exits if there are any
                # errors on parsing, so there's no need to handle this case
                # here as it will accomplish nothing
                pass
    except Exception as error:
        print_on_error(error)
        logger.error(str(error))
    finally:
        deinit()
        logger.shutdown()

if __name__ == '__main__':
    main()
