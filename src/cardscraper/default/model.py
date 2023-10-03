import re

from genanki import Model

from cardscraper.util import Conf

in_sbraces = re.compile(r'{{(.*?)}}')


def default_model(conf: Conf) -> Model:
    model_config = conf['model']
    special_fields = {
        'Tags',
        'Type',
        'Deck',
        'Subdeck',
        'CardFlag',
        'Card',
        'FrontSide',
    }

    css = model_config['css']
    id = model_config['id']
    name = model_config['name']

    templates = [{'name': k} | v for k, v in model_config['templates'].items()]

    fields = set()
    for template in templates:
        for side in ['qfmt', 'afmt']:
            a = in_sbraces.findall(template[side])
            fields.update(a)

    fields = fields.difference(special_fields)
    fields = [{'name': field} for field in fields]

    model = Model(id, name, fields, templates, css)
    print('Generated model!')
    return model
