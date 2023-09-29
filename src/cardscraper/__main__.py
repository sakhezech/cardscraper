import argparse
import json

from cardscraper.process_file import get_plugins, process_conf, read_yaml
from cardscraper.template import TEMPLATE
from cardscraper.version import VERSION


class Commands:
    @staticmethod
    def do_gen(args):
        if not args.json:
            for path in args.file:
                process_conf(read_yaml(path))
        else:
            for jsonstr in args.file:
                process_conf(json.loads(jsonstr))

    @staticmethod
    def do_init(args):
        for path in args.file:
            with open(path, 'w') as f:
                f.write(TEMPLATE)

    @staticmethod
    def do_list(_):
        plugins = get_plugins()
        for name, impls in plugins.items():
            print(f'{name.capitalize()} impls:')
            for entry in impls:
                print('-', entry.name)


def main():
    parser = argparse.ArgumentParser(
        prog='cardscraper',
        description='A tool for generating Anki cards by web scraping',
    )
    subparsers = parser.add_subparsers(dest='command')

    gen_parser = subparsers.add_parser(
        'gen',
        help='generate Anki package',
    )
    init_parser = subparsers.add_parser(
        'init',
        help='generate template file(s)',
    )
    subparsers.add_parser(
        'list',
        help='list available implementations',
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
