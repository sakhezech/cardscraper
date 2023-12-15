import argparse
import json
from typing import Any

import yaml

from cardscraper.__version__ import __version__
from cardscraper.generate import (
    Config,
    Step,
    find_plugins_and_generate,
    find_plugins_by_group,
)
from cardscraper.template import TEMPLATE


def read_yaml_file(path: str) -> Any:
    with open(path, 'r') as f:
        conf = yaml.load(f, yaml.Loader)
    return conf


class Commands:
    @staticmethod
    def do_gen(args):
        load_func = json.loads if args.json else read_yaml_file
        for f in args.file:
            conf: Config = load_func(f)
            find_plugins_and_generate(conf)

    @staticmethod
    def do_init(args):
        for path in args.file:
            with open(path, 'w') as f:
                f.write(TEMPLATE)

    @staticmethod
    def do_list(_):
        for step in Step:
            points = find_plugins_by_group(step)
            print(f'Available functions for {step}:')
            for point in points:
                print(f'  - {point.name}')

    @staticmethod
    def do_none(args):
        if args.version:
            print(__version__)


def main():
    parser = argparse.ArgumentParser(
        prog='cardscraper',
        description='A tool for generating Anki packages by webscraping',
    )
    subparsers = parser.add_subparsers(dest='command')

    gen_parser = subparsers.add_parser(
        'gen',
        help='generate Anki packages',
        description='Generates Anki packages from input files',
    )
    init_parser = subparsers.add_parser(
        'init',
        help='generate skeleton input files',
        description='Generates easily modifiable input file skeletons',
    )
    subparsers.add_parser(
        'list',
        help='list available functions',
        description='List all available functions for each step',
    )

    gen_parser.add_argument(
        'file',
        nargs='+',
        metavar='file',
        help='yaml input file(s)',
    )

    gen_parser.add_argument(
        '-j',
        '--json',
        action='store_true',
        help='pass json strings instead of files',
    )

    init_parser.add_argument(
        'file',
        nargs='+',
        metavar='file',
        help='file name(s)',
    )

    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='print program version and exit',
    )

    args = parser.parse_args()

    if args.command is None:
        args.command = 'none'

    getattr(Commands, 'do_' + args.command)(args)


if __name__ == '__main__':
    main()
