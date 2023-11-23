from importlib.metadata import EntryPoints, entry_points
from typing import Any, Callable, TypedDict

from genanki import Deck, Model, Note

MODULES = {'model', 'scraping', 'deck', 'package'}


def get_plugins() -> dict[str, EntryPoints]:
    return {
        module: entry_points(group=f'cardscraper.{module}')
        for module in MODULES
    }


class Config(TypedDict):
    meta: dict
    model: dict
    scraping: dict
    deck: dict
    package: dict
    args: Any


def find_plugins_and_generate(config: Config) -> None:
    plugins = get_plugins()

    if 'meta' not in config:
        config['meta'] = {}
    for module in MODULES:
        config['meta'].setdefault(module, 'default')

    meta = config['meta']

    impls = {
        f'do_{module}': plugins[module][meta[module]].load()
        for module in MODULES
    }

    generate_anki_package(config, **impls)


def generate_anki_package(
    config: Config,
    do_model: Callable[[Config], Model],
    do_scraping: Callable[[Config, Model], list[Note]],
    do_deck: Callable[[Config, list[Note]], Deck],
    do_package: Callable[[Config, Deck], None],
) -> None:
    model = do_model(config)
    notes = do_scraping(config, model)
    deck = do_deck(config, notes)
    do_package(config, deck)
