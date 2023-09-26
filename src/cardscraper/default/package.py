import os

from genanki import Deck, Package


def default_package(package_config, deck: Deck) -> None:
    name = package_config['name'].removesuffix('.apkg')
    out_path = package_config['output_path']
    media = [
        os.path.join(p, n)
        for p, _, ns in os.walk(package_config['media'])
        for n in ns
    ]
    package = Package(deck, media)
    os.makedirs(out_path, exist_ok=True)
    package.write_to_file(os.path.join(out_path, name + '.apkg'))
