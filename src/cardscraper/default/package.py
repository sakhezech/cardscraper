import logging
import os
from pathlib import Path

from genanki import Deck, Package

from cardscraper.generate import Config


def get_package(config: Config, deck: Deck) -> tuple[Package, Path]:
    package_config = config['package']
    name = package_config['name'].removesuffix('.apkg')
    output_path = package_config.setdefault('output', '.')
    media_path = package_config.setdefault('media', None)
    # pattern = package_config.setdefault('pattern', '**/*.*')

    # walking over the media folder and grabbing all files inside to put
    # in the package as media
    # TODO: Path.rglob(pattern='**/*.*') and add pattern to config
    if media_path:
        media = [
            os.path.join(p, n) for p, _, ns in os.walk(media_path) for n in ns
        ]
    else:
        media = []
    package = Package(deck, media)
    path = Path(os.path.join(output_path, name + '.apkg'))
    logger = logging.getLogger('cardscraper')
    logger.info('Generated package!')
    return package, path
