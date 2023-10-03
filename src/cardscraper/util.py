from importlib.metadata import EntryPoints, entry_points
from typing import Any, TypedDict

import yaml


def read_yaml(path: str) -> Any:
    with open(path, 'r') as f:
        conf = yaml.load(f, yaml.Loader)
    return conf


def get_plugins() -> dict[str, EntryPoints]:
    return {
        'model': entry_points(group='cardscraper.model'),
        'scraping': entry_points(group='cardscraper.scraping'),
        'deck': entry_points(group='cardscraper.deck'),
        'package': entry_points(group='cardscraper.package'),
    }


class Conf(TypedDict):
    meta: Any
    model: Any
    scraping: Any
    deck: Any
    package: Any
    args: Any
