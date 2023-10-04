import re

from genanki import Model, Note
from playwright.sync_api import ElementHandle, Page, sync_playwright

from cardscraper.util import Conf

Elem = Page | ElementHandle
InfoStorage = dict[str, str]


class Query:
    def __init__(
        self,
        name: str,
        query: str,
        all: bool = False,
        eval: str = '(e) => e.innerText',
        regex: str | None = None,
        format: str = '{}',
        children: dict | None = None,
    ) -> None:
        self.name = name
        self.query = query
        self.all = all
        self.eval = eval
        self.regex = regex
        self.format = format

        if children is None or not children:
            self.children: list[Query] = []
        else:
            self.children = [Query(k, **v) for k, v in children.items()]

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'({", ".join([f"{k}={v}" for k,v in self.__dict__.items()])})'
        )


def go_through_query(
    query: Query,
    handle: Elem,
    notes: list[Note],
    model: Model,
    info_storage: InfoStorage | None = None,
    saved_all: Query | None = None,
    saved_handle: Elem | None = None,
    original: bool = False,
) -> tuple[Query | None, Elem | None]:
    """
    Goes through the query recursively and appends the created notes to notes.

    RegEx has re.DOTALL enabled.
    """
    if info_storage is None:
        info_storage = {}

    if query.all:
        elems = handle.query_selector_all(query.query)
    else:
        elem = handle.query_selector(query.query)

        if elem is None:
            elems: list[ElementHandle] = []
        else:
            elems = [elem]

    for elem in elems:
        saved_all = saved_handle = None

        val = elem.evaluate(query.eval)
        if query.regex is not None:
            val = re.search(query.regex, val, re.DOTALL)
            if val is None:
                val = ''
            else:
                val = val.group(1)
        val = query.format.format(val)
        info_storage[query.name] = val

        for ch in query.children:
            if ch.all:
                if saved_all is not None:
                    raise ValueError(
                        'Having two or more all queries not under each other'
                        + ' is undefined behavior. The offending queries are '
                        + f'{saved_all.name} and {ch.name}'
                    )
                else:
                    saved_all = ch
                    saved_handle = elem
            else:
                return_all, return_handle = go_through_query(
                    ch,
                    elem,
                    notes,
                    model,
                    info_storage,
                    saved_all,
                    saved_handle,
                    original=False,
                )
                saved_all = saved_all or return_all
                saved_handle = saved_handle or return_handle

        if saved_all is None or saved_handle is None:
            if original:
                notes.append(make_note_from_storage(info_storage, model))
        else:
            if original:
                go_through_query(
                    saved_all,
                    saved_handle,
                    notes,
                    model,
                    info_storage,
                    original=True,
                )
    return saved_all, saved_handle


def make_note_from_storage(info_storage: InfoStorage, model: Model) -> Note:
    field_list = [field for fd in model.fields for _, field in fd.items()]
    fields_for_note = [info_storage[field] for field in field_list]

    return Note(model, fields_for_note)


def default_notes(conf: Conf, model: Model) -> list[Note]:
    scraping_config = conf['scraping']
    notes: list[Note] = []

    urls: list[str] = scraping_config['urls']
    queries = [Query(k, **v) for k, v in scraping_config['queries'].items()]

    with sync_playwright() as pw:
        print('Opening browser')
        browser = pw.chromium.launch()
        page = browser.new_page()
        for url in urls:
            print(f'Processing {url}')
            page.goto(url)
            for query in queries:
                go_through_query(query, page, notes, model, original=True)
    print('Generated notes!')
    return notes
