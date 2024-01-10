from enum import Enum
from importlib.metadata import EntryPoints, entry_points
from pathlib import Path
from typing import Callable

from genanki import Deck, Model, Note, Package

from cardscraper.config import Config


class StepName(str, Enum):
    """
    Names of the program steps.
    """

    def __str__(self) -> str:
        return self.value

    MODEL = 'model'
    SCRAPING = 'scraping'
    DECK = 'deck'
    PACKAGE = 'package'


def get_entrypoints_by_step(group: StepName) -> EntryPoints:
    """
    Gets a collection of function entry points by step name.

    Args:
        group (StepName): Name of the step, i.e. entry point group
            `cardscraper.x`.

    Returns:
        EntryPoints: Collection of function entry points.
    """
    return entry_points(group=f'cardscraper.{group}')


def select_function_by_step_and_name(group: StepName, name: str) -> Callable:
    """
    Gets a function by step name and function name.

    To get `mypackage:gen_model` from ::

        [project.entry-points.'cardscraper.model']
        my_impl = 'mypackage:gen_model'
        [project.entry-points.'cardscraper.scraping']
        my_impl = 'mypackage:gen_notes'
        [project.entry-points.'cardscraper.deck']
        my_impl = 'mypackage:gen_deck'
        [project.entry-points.'cardscraper.package']
        my_impl = 'mypackage:gen_package'

    call `select_function_by_step_and_name(Step.MODEL, 'my_impl')`

    Args:
        group (StepName): Name of the step, i.e. entry point group
            `cardscraper.x`.
        name (str): Function name.

    Returns:
        Callable: Selected function.
    """
    return get_entrypoints_by_step(group)[name].load()


def generate_anki_package_from_config_meta(
    config: Config,
) -> tuple[Package, Path]:
    """
    Generates an Anki package with automatically selected functions.

    Args:
        config (Config): Config dictionary.
    """
    if 'meta' not in config:
        config['meta'] = {}
    for module in StepName:
        config['meta'].setdefault(module, 'default')

    meta = config['meta']

    get_model = select_function_by_step_and_name(
        StepName.MODEL, meta[StepName.MODEL]
    )
    get_notes = select_function_by_step_and_name(
        StepName.SCRAPING, meta[StepName.SCRAPING]
    )
    get_deck = select_function_by_step_and_name(
        StepName.DECK, meta[StepName.DECK]
    )
    get_package = select_function_by_step_and_name(
        StepName.PACKAGE, meta[StepName.PACKAGE]
    )

    return generate_anki_package(
        config, get_model, get_notes, get_deck, get_package
    )


def generate_anki_package(
    config: Config,
    get_model: Callable[[Config], Model],
    get_notes: Callable[[Config, Model], list[Note]],
    get_deck: Callable[[Config, list[Note]], Deck],
    get_package: Callable[[Config, Deck], tuple[Package, Path]],
) -> tuple[Package, Path]:
    """
    Generates an Anki package with manually passed in functions.

    Args:
        config (Config): Config dictionary.
        get_model (Callable): Function that returns an Anki model from a
            config.
        get_notes (Callable): Function that returns a list of Anki notes from
            a config and a Anki model.
        get_deck (Callable): Function that returns an Anki deck from a config
            and a list of Anki notes.
        get_package (Callable): Function that returns an Anki package and a
            path to write it to from a config and an Anki deck.

    Returns:
        Package: Anki Package.
        Path: Path to save the package to.
    """
    model = get_model(config)
    notes = get_notes(config, model)
    deck = get_deck(config, notes)
    package, path = get_package(config, deck)
    return package, path


def write_package(package: Package, path: Path) -> None:
    """
    Writes an Anki package to a path.

    Args:
        package (Package): Anki Package.
        path (Path): Path to save the package to.
    """
    path.parent.mkdir(exist_ok=True)
    package.write_to_file(path)
