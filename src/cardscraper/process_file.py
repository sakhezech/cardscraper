from importlib.metadata import entry_points

import yaml


def process_file(path: str):
    conf = read_yaml(path)
    process_conf(conf)


def read_yaml(path: str):
    with open(path, 'r') as f:
        conf = yaml.load(f, yaml.Loader)
    return conf


def get_plugins():
    return {
        'model': entry_points(group='cardscraper.model'),
        'scraping': entry_points(group='cardscraper.scraping'),
        'deck': entry_points(group='cardscraper.deck'),
        'package': entry_points(group='cardscraper.package'),
    }


def process_conf(conf) -> None:

    plugins = get_plugins()
    model_plugins = plugins['model']
    notes_plugins = plugins['scraping']
    deck_plugins = plugins['deck']
    package_plugins = plugins['package']

    meta_config = conf['meta']

    get_model = model_plugins[meta_config['model']].load()
    get_notes = notes_plugins[meta_config['scraping']].load()
    get_deck = deck_plugins[meta_config['deck']].load()
    packaging = package_plugins[meta_config['package']].load()

    process_conf_manual(conf, get_model, get_notes, get_deck, packaging)


def process_conf_manual(
    conf, get_model, get_notes, get_deck, packaging
) -> None:
    model_config = conf['model']
    scraping_config = conf['scraping']
    deck_cofig = conf['deck']
    package_config = conf['package']

    model = get_model(model_config)
    notes = get_notes(scraping_config, model)
    deck = get_deck(deck_cofig)
    deck.notes.extend(notes)
    packaging(package_config, deck)
