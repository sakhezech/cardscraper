import re

from genanki import Model


def get_model(model_config) -> Model:
    special_fields = {
        'Tags',
        'Type',
        'Deck',
        'Subdeck',
        'CardFlag',
        'Card',
        'FrontSide',
    }

    in_sbrackets = re.compile(r'{{(.*?)}}')
    css = model_config['css']
    id = model_config['id']
    name = model_config['name']

    templates = [{'name': k} | v for k, v in model_config['templates'].items()]

    fields = set()
    for template in templates:
        for side in ['qfmt', 'afmt']:
            a = in_sbrackets.findall(template[side])
            fields.update(a)

    fields = fields.difference(special_fields)
    fields = [{'name': field} for field in fields]

    return Model(id, name, fields, templates, css)
