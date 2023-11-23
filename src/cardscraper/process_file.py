from importlib.metadata import EntryPoints, entry_points
from typing import Any, Callable, TypedDict

from genanki import Deck, Model, Note


def get_plugins() -> dict[str, EntryPoints]:
    return {
        'model': entry_points(group='cardscraper.model'),
        'scraping': entry_points(group='cardscraper.scraping'),
        'deck': entry_points(group='cardscraper.deck'),
        'package': entry_points(group='cardscraper.package'),
    }


class Config(TypedDict):
    meta: Any
    model: Any
    scraping: Any
    deck: Any
    package: Any
    args: Any


def find_plugins_and_generate(config: Config) -> None:
    plugins = get_plugins()
    model_plugins = plugins['model']
    notes_plugins = plugins['scraping']
    deck_plugins = plugins['deck']
    package_plugins = plugins['package']

    meta_config = config['meta']

    get_model = model_plugins[meta_config['model']].load()
    get_notes = notes_plugins[meta_config['scraping']].load()
    get_deck = deck_plugins[meta_config['deck']].load()
    packaging = package_plugins[meta_config['package']].load()

    generate_anki_package(config, get_model, get_notes, get_deck, packaging)


def generate_anki_package(
    config: Config,
    get_model: Callable[[Config], Model],
    get_notes: Callable[[Config, Model], list[Note]],
    get_deck: Callable[[Config, list[Note]], Deck],
    packaging: Callable[[Config, Deck], None],
) -> None:
    model = get_model(config)
    notes = get_notes(config, model)
    deck = get_deck(config, notes)
    packaging(config, deck)
