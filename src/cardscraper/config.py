from typing import TypedDict


class MetaConfig(TypedDict):
    model: str
    scraping: str
    deck: str
    package: str


class DeckConfig(TypedDict):
    id: int
    name: str


class ModelConfig(TypedDict):
    id: int
    name: str
    templates: list[dict]
    css: str


class ScrapingConfig(TypedDict):
    urls: list[str]
    agent: str
    queries: list[dict]


class PackageConfig(TypedDict):
    name: str
    output: str
    media: str | None
    pattern: str


class Config(TypedDict):
    """
    TODO: Write docs and make subdicts typed too.
    """

    meta: MetaConfig
    model: ModelConfig
    scraping: ScrapingConfig
    deck: DeckConfig
    package: PackageConfig


def set_config_defaults(config: Config) -> Config:
    """
    Mutates config!
    """

    model_config = config['model']
    model_config.setdefault('css', '')

    package_config = config['package']
    package_config.setdefault('output', '.')
    package_config.setdefault('media', None)
    package_config.setdefault('pattern', '**/*.*')

    scraping_config = config['scraping']
    scraping_config.setdefault(
        'agent',
        (
            'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) '
            'Gecko/20100101 Firefox/120.0'
        ),
    )

    return config
