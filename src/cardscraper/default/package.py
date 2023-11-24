import os

from genanki import Deck, Package

from cardscraper.generate import Config


def default_package(config: Config, deck: Deck) -> None:
    package_config = config['package']
    name = package_config['name'].removesuffix('.apkg')
    output_path = package_config.setdefault('output', '.')
    media_path = package_config.setdefault('media', None)

    if media_path:
        media = [
            os.path.join(p, n) for p, _, ns in os.walk(media_path) for n in ns
        ]
    else:
        media = []
    package = Package(deck, media)
    os.makedirs(output_path, exist_ok=True)
    package.write_to_file(os.path.join(output_path, name + '.apkg'))
    print('Completed packaging!\nDone!')
