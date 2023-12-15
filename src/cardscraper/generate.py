from enum import Enum
from importlib.metadata import EntryPoints, entry_points
from typing import Callable, TypedDict

from genanki import Deck, Model, Note


class Step(str, Enum):
    def __str__(self) -> str:
        return self.value

    MODEL = 'model'
    SCRAPING = 'scraping'
    DECK = 'deck'
    PACKAGE = 'package'


def find_plugins_by_group(group: Step) -> EntryPoints:
    return entry_points(group=f'cardscraper.{group}')


def get_function_by_group_and_name(group: Step, name: str) -> Callable:
    return find_plugins_by_group(group)[name].load()


class Config(TypedDict):
    meta: dict
    model: dict
    scraping: dict
    deck: dict
    package: dict


def find_plugins_and_generate(config: Config) -> None:
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
    package = get_function_by_group_and_name(Step.PACKAGE, meta[Step.PACKAGE])

    generate_anki_package(config, get_model, get_notes, get_deck, package)


def generate_anki_package(
    config: Config,
    get_model: Callable[[Config], Model],
    get_notes: Callable[[Config, Model], list[Note]],
    get_deck: Callable[[Config, list[Note]], Deck],
    package: Callable[[Config, Deck], None],
) -> None:
    model = get_model(config)
    notes = get_notes(config, model)
    deck = get_deck(config, notes)
    package(config, deck)
