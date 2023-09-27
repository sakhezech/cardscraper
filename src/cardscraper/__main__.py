import argparse
import json

from cardscraper.process_file import process_conf, process_file


def main():
    parser = argparse.ArgumentParser(
        prog='cardscraper',
        description='A tool for generating Anki cards by web scraping',
    )

    parser.add_argument(
        'file',
        nargs='+',
        metavar='file',
        help='yaml instruction file(s)',
    )

    parser.add_argument(
        '-j',
        '--json',
        action='store_true',
        help='pass json strings instead of files',
    )

    args = parser.parse_args()

    if not args.json:
        for path in args.file:
            process_file(path)
    else:
        for jsonstr in args.file:
            process_conf(json.loads(jsonstr))


if __name__ == '__main__':
    main()
