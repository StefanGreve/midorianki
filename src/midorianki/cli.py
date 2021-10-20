#!/usr/bin/env python3

import argparse
import errno
import sys
from collections import namedtuple
from pathlib import Path

from . import config, midorianki, utils
from .__init__ import __version__, package_description, package_name


def cli():
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=52)
    parser = argparse.ArgumentParser(prog=package_name, formatter_class=formatter, description=package_description)
    parser._positionals.title = 'Commands'
    parser._optionals.title = 'Arguments'

    parser.add_argument('--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('--verbose', default=True, action='store_true', help="increase output verbosity (default: %(default)s)")
    parser.add_argument('--no-verbose', dest='verbose', action='store_false', help="run commands silently")

    subparser = parser.add_subparsers(dest='command')

    convert_help_msg = "convert CSV files into APKG decks"
    convert_parser = subparser.add_parser('convert', description=convert_help_msg, help=convert_help_msg)
    convert_parser.add_argument('--file', type=Path, metavar='PATH', required=True, help="path to CSV file")
    convert_parser.add_argument('--dest', type=Path, metavar='PATH', nargs='?', default=Path.cwd(), help="APKG target directory (default: %(default)s)")
    convert_parser.add_argument('--name', type=str, nargs='?', default=None, help="deck filename and title") # TODO: default value?

    log_help_msg = "access the CLI logger"
    log_parser = subparser.add_parser('log', description=log_help_msg, help=log_help_msg)
    log_parser.add_argument('--reset', action='store_true', help="reset all log file entries")
    log_parser.add_argument('--path', action='store_true', help="return the log file path")
    log_parser.add_argument('--list', action='store_true', help='read the log file')

    args = parser.parse_args()

    try:
        if args.command == 'convert':
            midorianki.export(args.file, args.name, args.dest, args.verbose)
            pass

        if args.command == 'log':
            logfile = utils.get_resource_path(config.LOGFILE)

            if args.path:
                return logfile
            if args.reset:
                utils.reset_file(logfile)
                return
            if args.list:
                with open(logfile, mode='r', encoding='utf-8') as file_handler:
                    log = file_handler.readlines()

                    if not log:
                        utils.print_on_warning("There is nothing to read because the log file is empty")
                        return

                    parse = lambda line: line.strip('\n').split('::')
                    Entry = namedtuple('Entry', 'timestamp levelname lineno name message')

                    tabulate = "{:<20} {:<5} {:<6} {:<18} {:<20}".format

                    print('\n' + config.GREEN + tabulate('Timestamp', 'Line', 'Level', 'File Name', 'Message') + config.RESET_ALL)

                    for line in log:
                        entry = Entry(parse(line)[0], parse(line)[1], parse(line)[2], parse(line)[3], parse(line)[4])
                        print(tabulate(entry.timestamp, entry.lineno.zfill(4), entry.levelname, entry.name, entry.message))

                    print()

    except Exception as error:
        print(f"\n{config.RED}ERROR:{config.RESET_ALL} {error}", file=sys.stderr)
        utils.logger.error(str(error))
        sys.stderr(errno.EINVAL)
