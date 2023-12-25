import argparse
from typing import Sequence

import yaml

from cardscraper.__version__ import __version__
from cardscraper.generate import (
    Config,
    Step,
    find_plugins_by_group,
    generate_from_config,
)
from cardscraper.template import TEMPLATE


def cli(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        prog='cardscraper',
        description='A tool for generating Anki packages by webscraping',
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__,
    )

    subparsers = parser.add_subparsers(dest='command')

    gen_parser = subparsers.add_parser(
        'gen',
        help='generate Anki packages',
        description='Generates Anki packages from input files',
    )

    gen_parser.add_argument(
        'file',
        nargs='+',
        metavar='file',
        type=argparse.FileType(),
        help='yaml input file(s)',
    )

    init_parser = subparsers.add_parser(
        'init',
        help='generate skeleton input files',
        description='Generates easily modifiable input file skeletons',
    )

    init_parser.add_argument(
        'file',
        nargs='+',
        metavar='file',
        type=argparse.FileType('w'),
        help='file name(s)',
    )

    subparsers.add_parser(
        'list',
        help='list available functions',
        description='List all available functions for each step',
    )

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return

    match args.command:
        case 'gen':
            for file in args.file:
                conf: Config = yaml.load(file, yaml.Loader)
                generate_from_config(conf)
        case 'init':
            for file in args.file:
                file.write(TEMPLATE)
        case 'list':
            for step in Step:
                points = find_plugins_by_group(step)
                print(f'Available functions for {step}:')
                for point in points:
                    print(f'  - {point.name}')


if __name__ == '__main__':
    cli()
