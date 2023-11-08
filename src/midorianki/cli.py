#!/usr/bin/env python3

from argparse import ArgumentParser, HelpFormatter
from pathlib import Path


def build_parser(package_name: str, version: str, description: str) -> ArgumentParser:
    formatter = lambda prog: HelpFormatter(prog,max_help_position=52)
    parser = ArgumentParser(prog=package_name, description=description, formatter_class=formatter)
    parser._positionals.title = "Commands"
    parser._optionals.title = "Arguments"

    parser.add_argument('--version', action='version', version=f"%(prog)s {version}")
    parser.add_argument('--verbose', default=True, action='store_true', help="increase output verbosity (default: %(default)s)")
    parser.add_argument('--no-verbose', dest='verbose', action='store_false', help="run commands silently")

    subparser = parser.add_subparsers(dest='command')

    convert_help_msg = "convert CSV files into APKG decks"
    convert_parser = subparser.add_parser('convert', description=convert_help_msg, help=convert_help_msg)
    convert_parser.add_argument('--file', type=Path, metavar='PATH', required=True, help="path to CSV file")
    convert_parser.add_argument('--dest', type=Path, metavar='PATH', nargs='?', default=Path.cwd(), help="APKG target directory (default: %(default)s)")
    convert_parser.add_argument('--name', type=str, nargs='?', default=None, help="deck filename and title (default: file stem)")

    return parser
