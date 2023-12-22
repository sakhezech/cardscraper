import pytest
from cardscraper import Config
from genanki.model import yaml


@pytest.fixture
def config() -> Config:
    with open('tests/config.yaml', 'r') as f:
        config: Config = yaml.load(f, yaml.Loader)
    return config
