from genanki import Deck


def get_deck(deck_config) -> Deck:
    return Deck(**deck_config)
