# cardscraper

`cardscraper` is a tool for generating Anki packages by webscraping.

## use me

install `cardscraper` from [PyPI](https://pypi.org/project/cardscraper/)

```
pip install cardscraper
```

generate a skeleton input file

```
cardscraper init hello.yaml
```

edit the file and generate the Anki package

```
cardscraper gen hello.yaml
```

## editing the file

`cardscraper` takes in YAML files as input

#### quick example

[go down](#full-explanation) for an in-depth one

```yaml
scraping:
  urls:
    - https://www.scrapethissite.com/pages/simple/
  queries:
    - name: Entry
      query: .country
      many: true
      children:
        - name: Info
          query: .country-info
        - name: Name
          query: .country-name

model:
  name: My Model
  id: 123 # make this unique
  templates:
    - name: My Card Template
      qfmt: |
        {{Info}}
      afmt: |
        {{FrontSide}}
        <hr id='answer'>
        {{Name}}

deck:
  name: My Deck
  id: 987 # make this unique

package:
  name: sample_package.apkg
  output: ./output/
```

#### full explanation

```yaml
# here you can specify which module to use for each step
# (every one defaults to 'default')
meta:
  # controls package details and package dumping
  package: default
  # controls deck creation
  deck: default
  # controls model creation
  model: default
  # controls scraping and note creation
  scraping: default

# anki package info
package:
  # package name
  name: package_name
  # output folder (defaults to '.')
  output: ./out/
  # media folder (defaults to null)
  # every file in the directory will be added to the package as media
  media: ./media/

# anki deck info
deck:
  # deck name
  name: Deck
  # deck id
  # don't forget to make this value unique
  id: 987

# anki model info
model:
  # model name
  name: Model
  # model id
  # don't forget to make this value unique
  id: 321
  # card styling (defaults to '')
  css: |
    .question, .answer {
        text-align: center;
    }
    .question {
        font-size: 5rem;
        font-weight: 700;
    }
    .answer {
        font-size: 3rem;
    }
  # list of cards
  templates:
    # card name
    - name: Front
      # front side
      qfmt: |
        <div class='question'>
        {{Question}}
        </div>
      # back side
      afmt: |
        {{FrontSide}}
        <hr id='answer'>
        <div class='answer'>
        {{Answer}}
        </div>
    # same here
    - name: Back
      qfmt: |
        <div class='question'>
        {{Answer}}
        </div>
      afmt: |
        {{FrontSide}}
        <hr id='answer'>
        <div class='answer'>
        {{Question}}
        </div>

# scraping info
scraping:
  # list of urls to scrape
  urls:
    - https://www.scrapethissite.com/pages/simple/
  # you can set your own custom user agent (defaults to the one here)
  agent: Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0
  # list of queries
  # each query selects an html element and lets you use its text in the templates
  # each child query runs inside the parent one
  queries:
    # query name which you can use in the templates like {{Country}}
    - name: Country
      # css selector
      query: .country
      # you can select something specific from the query by providing a regex
      # this is a python regex with re.DOTALL enabled i.e. '.' captures '\n'
      # uses the first captured group
      # (defaults to null)
      regex: null
      # if true: we select every instance and iterate over them
      # if false: we only select the first one
      # basically it's querySelector() vs querySelectorAll()
      # (defaults to false)
      many: true
      children:
        - name: Question
          query: .country-info
          many: false
          regex: (Area .*)$
          children: null
        - name: Answer
          query: .country-name
          many: false
          regex: null
          children: null
```

## using in code

```py
from cardscraper import generate_anki_package, get_plugin_by_group_and_name
from cardscraper.__main__ import read_yaml_file
from cardscraper.generate import Config, Module
from genanki import Model, Note

if __name__ == '__main__':
    config = read_yaml_file('/path/to/config.yaml')
    # or
    # config: Config = {...}

    get_model = get_plugin_by_group_and_name(Module.MODEL, 'default')
    get_deck = get_plugin_by_group_and_name(Module.DECK, 'default')
    get_package = get_plugin_by_group_and_name(Module.PACKAGE, 'default')

    def get_notes(config: Config, model: Model) -> list[Note]:
        notes = []
        ...
        return notes

    generate_anki_package(config, get_model, get_notes, get_deck, get_package)
```

## plugin system

you can add custom modules by exposing `cardscraper.x` entry point in your package

```toml
[project.entry-points.'cardscraper.model']
my_impl = 'mypackage:gen_model'
[project.entry-points.'cardscraper.scraping']
my_impl = 'mypackage:gen_notes'
[project.entry-points.'cardscraper.deck']
my_impl = 'mypackage:gen_deck'
[project.entry-points.'cardscraper.package']
my_impl = 'mypackage:gen_package'
```
