"""
A tool for generating Anki packages by webscraping.

Takes in YAML input files and returns an Anki package based
on its instructions/contents.
This is primarily a CLI tool, but *can* be used inside code.
For the explanation of the YAML input files please read `cardscraper.Config`
docstring.

Typical usage example: ::

    $ cardscraper init hello.yaml
    $ nvim hello.yaml
    ...
    $ cardscraper gen hello.yaml
"""
from cardscraper.config import Config
from cardscraper.generate import (
    Step,
    find_plugins_by_group,
    generate_anki_package,
    generate_from_config,
    get_function_by_group_and_name,
)

__all__ = [
    'Config',
    'Step',
    'find_plugins_by_group',
    'generate_from_config',
    'generate_anki_package',
    'get_function_by_group_and_name',
]
