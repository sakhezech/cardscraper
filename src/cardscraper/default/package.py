import os

from genanki import Deck, Package

from cardscraper.util import Conf


def default_package(conf: Conf, deck: Deck) -> None:
    package_config = conf['package']
    name = package_config['name'].removesuffix('.apkg')
    out_path = package_config['output_path']
    if package_config.setdefault('media', None):
        media = [
            os.path.join(p, n)
            for p, _, ns in os.walk(package_config['media'])
            for n in ns
        ]
    else:
        media = []
    package = Package(deck, media)
    os.makedirs(out_path, exist_ok=True)
    package.write_to_file(os.path.join(out_path, name + '.apkg'))
    print('Completed packaging!\nDone!')
