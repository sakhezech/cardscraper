from genanki import Deck

from cardscraper.util import Conf


def default_deck(conf: Conf) -> Deck:
    deck_config = conf['deck']
    id = deck_config['id']
    name = deck_config['name']
    deck = Deck(id, name)
    print('Generated deck!')
    return deck
