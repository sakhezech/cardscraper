from enum import Enum
from importlib.metadata import EntryPoints, entry_points
from pathlib import Path
from typing import Callable, TypedDict

from genanki import Deck, Model, Note, Package


class Step(str, Enum):
    def __str__(self) -> str:
        return self.value

    MODEL = 'model'
    SCRAPING = 'scraping'
    DECK = 'deck'
    PACKAGE = 'package'


def find_plugins_by_group(group: Step) -> EntryPoints:
    """
    Gets the collection of function entry points by step name.

    Args:
        group (Step): name of the step, i.e. entry point group `cardscraper.x`

    Returns:
        EntryPoints: collection of function entry points
    """
    return entry_points(group=f'cardscraper.{group}')


def get_function_by_group_and_name(group: Step, name: str) -> Callable:
    """
    Gets the function by group name and func name.

    To get `mypackage:gen_model` from ::

        [project.entry-points.'cardscraper.model']
        my_impl = 'mypackage:gen_model'
        [project.entry-points.'cardscraper.scraping']
        my_impl = 'mypackage:gen_notes'
        [project.entry-points.'cardscraper.deck']
        my_impl = 'mypackage:gen_deck'
        [project.entry-points.'cardscraper.package']
        my_impl = 'mypackage:gen_package'

    call `get_function_by_group_and_name(Step.MODEL, 'my_impl')`

    Args:
        group (Step): name of the step, i.e. entry point group `cardscraper.x`
        name (str): function name

    Returns:
        Callable: selected function
    """
    return find_plugins_by_group(group)[name].load()


class Config(TypedDict):
    meta: dict
    model: dict
    scraping: dict
    deck: dict
    package: dict


def generate_from_config(config: Config) -> None:
    """
    Finds the correct functions and generates and writes an Anki package.

    Looks into the config's 'meta' section and calls `generate_anki_package`

    Args:
        config (Config): Config dictionary that has all the instructions for
            all the found functions

    Returns:
        None
    """
    if 'meta' not in config:
        config['meta'] = {}
    for module in Step:
        config['meta'].setdefault(module, 'default')

    meta = config['meta']

    get_model = get_function_by_group_and_name(Step.MODEL, meta[Step.MODEL])
    get_notes = get_function_by_group_and_name(
        Step.SCRAPING, meta[Step.SCRAPING]
    )
    get_deck = get_function_by_group_and_name(Step.DECK, meta[Step.DECK])
    get_package = get_function_by_group_and_name(
        Step.PACKAGE, meta[Step.PACKAGE]
    )

    generate_anki_package(config, get_model, get_notes, get_deck, get_package)


def generate_anki_package(
    config: Config,
    get_model: Callable[[Config], Model],
    get_notes: Callable[[Config, Model], list[Note]],
    get_deck: Callable[[Config, list[Note]], Deck],
    get_package: Callable[[Config, Deck], tuple[Package, Path]],
) -> None:
    """
    Generates and writes an Anki package with manually passed in functions.

    Args:
        config (Config): Config dictionary that has all the instructions for
            all the functions below
        get_model (Callable): function that returns an Anki model from a config
        get_notes (Callable): function that returns a list of Anki notes from
            a config and a Anki model
        get_deck (Callable): function that returns an Anki deck from a config
            and a list of Anki notes
        get_package (Callable): function that returns an Anki package and the
            path to write it to from a config and an Anki deck

    Returns:
        None
    """
    model = get_model(config)
    notes = get_notes(config, model)
    deck = get_deck(config, notes)
    package, path = get_package(config, deck)

    path.parent.mkdir(exist_ok=True)
    package.write_to_file(path)
