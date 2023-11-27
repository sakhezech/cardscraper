import re

import requests
from bs4 import BeautifulSoup, Tag
from genanki import Model, Note

from cardscraper.generate import Config


class Query:
    def __init__(
        self,
        name: str,
        query: str,
        many: bool = False,
        regex: str | None = None,
        children: dict | None = None,
    ) -> None:
        if children is None:
            children = {}
        self.name = name
        self.query = query
        self.many = many
        self.regex = regex
        self.children = [Query(**child) for child in children]


def generate_notes_for_quote(
    tag: Tag,
    query: Query,
    model: Model,
    notes: list[Note] | None = None,
    info: dict | None = None,
) -> list[Note]:
    if notes is None:
        notes = []
    if info is None:
        info = {}

    selected_tags = tag.select(query.query)
    # non 'many' queries only get the first selected tag
    if not query.many and selected_tags:
        selected_tags = selected_tags[:1]

    for selected_tag in selected_tags:
        if query.regex is not None:
            text = re.search(query.regex, selected_tag.text, re.DOTALL)
            if text is None:
                text = ''
            else:
                text = text.group(1)
            info[query.name] = text
        else:
            info[query.name] = selected_tag.text

        normal_queries = [q for q in query.children if not q.many]
        many_queries = [q for q in query.children if q.many]

        # this ensures that 'many' query will be processed last
        for child in normal_queries + many_queries:
            generate_notes_for_quote(selected_tag, child, model, notes, info)

        if not many_queries and query.many:
            notes.append(make_note_from_info(info, model))

    return notes


def make_note_from_info(info: dict, model: Model) -> Note:
    model_field_names = [
        field_name for fd in model.fields for _, field_name in fd.items()
    ]
    fields_for_note = [info[field_name] for field_name in model_field_names]
    return Note(model, fields_for_note)


def validate_query_tree(query: Query) -> bool:
    queries_with_many_under = [
        validate_query_tree(child) for child in query.children
    ].count(True)
    if queries_with_many_under > 1:
        raise ValueError(
            "Having two or more 'many' queries not "
            'under each other is undefined behavior.'
        )
    return query.many | bool(queries_with_many_under)


def default_notes(config: Config, model: Model) -> list[Note]:
    scraping_config = config['scraping']
    urls = scraping_config['urls']
    agent = scraping_config.setdefault(
        'agent',
        (
            'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) '
            'Gecko/20100101 Firefox/120.0'
        ),
    )

    headers = {'User-Agent': agent}

    queries = [Query(**child) for child in scraping_config['queries']]
    for query in queries:
        validate_query_tree(query)
    notes = []
    for url in urls:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        for query in queries:
            notes.extend(generate_notes_for_quote(soup, query, model))
    print('Generated notes!')
    return notes
