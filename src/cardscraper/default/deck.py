from genanki import Deck, Note

from cardscraper.generate import Config


def default_deck(config: Config, notes: list[Note]) -> Deck:
    deck_config = config['deck']
    id = deck_config['id']
    name = deck_config['name']

    deck = Deck(id, name)
    deck.notes.extend(notes)
    print('Generated deck!')
    return deck
