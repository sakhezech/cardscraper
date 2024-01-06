from typing import TypedDict


class Config(TypedDict):
    """
    TODO: Write docs and make subdicts typed too.
    """

    meta: dict
    model: dict
    scraping: dict
    deck: dict
    package: dict
