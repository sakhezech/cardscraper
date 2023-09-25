import yaml

from cardscraper.default.deck import get_deck
from cardscraper.default.model import get_model
from cardscraper.default.package import package
from cardscraper.default.scraping import get_notes


def process_file(path: str) -> None:

    with open(path, 'r') as f:
        conf = yaml.load(f, yaml.Loader)

    model_config = conf['model']
    deck_cofig = conf['deck']
    package_config = conf['package']
    scraping_config = conf['scraping']

    model = get_model(model_config)
    notes = get_notes(scraping_config, model)
    deck = get_deck(deck_cofig)
    deck.notes.extend(notes)
    package(package_config, deck)
