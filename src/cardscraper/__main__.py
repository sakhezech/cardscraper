import argparse
import json

from cardscraper.process_file import process_conf
from cardscraper.template import TEMPLATE
from cardscraper.util import Conf, get_plugins, read_yaml
from cardscraper.version import VERSION


class Commands:
    @staticmethod
    def do_gen(args):
        load_func = json.loads if args.json else read_yaml
        for f in args.file:
            conf: Conf = load_func(f)
            conf['args'] = args
            process_conf(conf)

    @staticmethod
    def do_init(args):
        for path in args.file:
            with open(path, 'w') as f:
                f.write(TEMPLATE)

    @staticmethod
    def do_list(_):
        plugins = get_plugins()
        for name, impls in plugins.items():
            print(f'{name.capitalize()} implementations:')
            for entry in impls:
                print('    -', entry.name)


def main():
    parser = argparse.ArgumentParser(
        prog='cardscraper',
        description='A tool for generating Anki cards by web scraping',
    )
    subparsers = parser.add_subparsers(dest='command')

    gen_parser = subparsers.add_parser(
        'gen',
        help='generate Anki packages',
        description='Generates Anki packages from YAML instruction files',
    )
    init_parser = subparsers.add_parser(
        'init',
        help='generate template files',
        description='Generates easily modifiable '
        'YAML instruction file templates',
    )
    subparsers.add_parser(
        'list',
        help='list available implementations',
        description='Lists all available implementations',
    )

    gen_parser.add_argument(
        'file',
        nargs='+',
        metavar='file',
        help='yaml instruction file(s)',
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
        help='print program version',
    )

    args = parser.parse_args()

    if args.command is not None:
        getattr(Commands, 'do_' + args.command)(args)
    else:
        if args.version:
            print(VERSION)
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
