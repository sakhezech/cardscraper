from typing import Callable

from genanki import Deck, Model, Note

from cardscraper.util import Conf, get_plugins


def process_conf(conf: Conf) -> None:

    plugins = get_plugins()
    model_plugins = plugins['model']
    notes_plugins = plugins['scraping']
    deck_plugins = plugins['deck']
    package_plugins = plugins['package']

    meta_config = conf['meta']

    get_model = model_plugins[meta_config['model']].load()
    get_notes = notes_plugins[meta_config['scraping']].load()
    get_deck = deck_plugins[meta_config['deck']].load()
    packaging = package_plugins[meta_config['package']].load()

    process_conf_manual(conf, get_model, get_notes, get_deck, packaging)


def process_conf_manual(
    conf: Conf,
    get_model: Callable[[Conf], Model],
    get_notes: Callable[[Conf, Model], list[Note]],
    get_deck: Callable[[Conf, list[Note]], Deck],
    packaging: Callable[[Conf, Deck], None],
) -> None:
    model = get_model(conf)
    notes = get_notes(conf, model)
    deck = get_deck(conf, notes)
    packaging(conf, deck)
