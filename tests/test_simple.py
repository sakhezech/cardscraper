from cardscraper.default import get_deck, get_model
from cardscraper.generate import Config
from genanki import Note


def test_deck(config: Config):
    note_list = [Note(), Note()]
    deck = get_deck(config, note_list)

    assert deck.notes == note_list
    assert deck.deck_id == config['deck']['id']
    assert deck.name == config['deck']['name']


def test_model(config: Config):
    model = get_model(config)
    sorted_fields = sorted(model.fields, key=lambda x: x['name'])

    assert sorted_fields == [{'name': 'Answer'}, {'name': 'Question'}]
    assert model.model_id == config['model']['id']
    assert model.name == config['model']['name']
    assert model.css == config['model']['css']
    assert model.templates == [
        {
            'name': 'Front',
            'qfmt': "<div class='question'>\n{{Question}}\n</div>\n",
            'afmt': "{{FrontSide}}\n<hr id='answer'>\n"
            "<div class='answer'>\n{{Answer}}\n</div>\n",
        }
    ]


def test_package(config: Config):
    pass
