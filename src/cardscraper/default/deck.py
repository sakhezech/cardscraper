from genanki import Deck, Note

from cardscraper.util import Config


def default_deck(conf: Config, notes: list[Note]) -> Deck:
    deck_config = conf['deck']
    id = deck_config['id']
    name = deck_config['name']
    deck = Deck(id, name)
    deck.notes.extend(notes)
    print('Generated deck!')
    return deck
