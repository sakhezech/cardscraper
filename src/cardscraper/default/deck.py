from genanki import Deck


def default_deck(deck_config) -> Deck:
    id = deck_config['id']
    name = deck_config['name']
    deck = Deck(id, name)
    print('Generated deck!')
    return deck
