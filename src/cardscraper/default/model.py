import logging
import re

from genanki import Model

from cardscraper.generate import Config

in_sbraces = re.compile(r'{{(.*?)}}')


def get_model(config: Config) -> Model:
    model_config = config['model']
    id = model_config['id']
    name = model_config['name']
    css = model_config.setdefault('css', '')
    templates = model_config['templates']

    special_fields = {
        'Tags',
        'Type',
        'Deck',
        'Subdeck',
        'CardFlag',
        'Card',
        'FrontSide',
    }
    fields = set()
    for template in templates:
        for side in ['qfmt', 'afmt']:
            a = in_sbraces.findall(template[side])
            fields.update(a)

    fields = fields.difference(special_fields)
    fields = [{'name': field} for field in fields]

    model = Model(id, name, fields, templates, css)
    logger = logging.getLogger('cardscraper')
    logger.info('Generated model!')
    return model
