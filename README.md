# cardscraper

A tool for generating Anki cards by web scraping

## Installation

### with pip

```
python3 -m pip install cardscraper
```

### with [pipx](https://pypa.github.io/pipx/)

```
pipx install --include-deps cardscraper
```

## [Playwright](https://github.com/microsoft/playwright)

cardscraper uses Playwright for scraping by default; you will need to install
Chromium

```
playwright install chromium
```

## Usage

`cardscraper ...` or `python3 -m cardscraper ...`

cardscraper has 3 main subcommands:

- `cardscraper gen` - takes in [yaml instruction files](#yaml-instruction-file)
  and generates Anki packages
- `cardscraper init` - generates [yaml instruction file](#yaml-instruction-file)
  templates
- `cardscraper list` - lists all available module implementations

and you can always use `cardscraper <subcommand> -h`

I recommend doing something like:

1. `cardscraper init hello.yaml`
2. edit the file to suit your needs
3. `cardscraper gen hello.yaml`

## YAML instruction file

```yaml
# Meta defines which functions will take care of each step
# Get list of available implementations from 'cardscraper list'
meta:
  package: default
  deck: default
  model: default
  scraping: default

package:
  # Output package name
  name: sample_package
  # Output folder
  output_path: ./out/
  # Path to the media folder where 'all to include' media files are
  # Defaults to null
  media: null

deck:
  # Deck name
  name: Countries
  # Deck ID
  id: 84269713

model:
  # Model name
  name: Countries Model
  # Model ID
  id: 97138426
  # CSS styling
  css: |
    * {
        color: #333;
        background-color: #fffffa;
    }
    .q, .a {
        text-align: center;
    }
    .q {
        font-size: 5rem;
        font-weight: 700;
    }
    .a {
        font-size: 3rem;
    }
  # Templates
  templates:
    CountryToInfo: # Template name
      # Front template
      # Note that you can use query output by {{QueryName}}
      qfmt: |
        <div class='q'>
            {{Country}}
        </div>
      # Back template
      afmt: |
        {{FrontSide}}
        <hr id=answer>
        <div class='a'>
            {{Info}}
            <a href="https://en.wikipedia.org/w/index.php?search={{Country}}">
                more info
            </a>
        </div>
    CapitalToCountry:
      qfmt: |
        <div class='q'>
            {{Capital}}
        </div>
      afmt: |
        {{FrontSide}}
        <hr id=answer>
        <div class='a'>
            {{Country}}<br>
            <a href="https://en.wikipedia.org/w/index.php?search={{Capital}}">
                more info
            </a>
        </div>

scraping:
  # List of URLs to scrape
  urls:
    - https://www.scrapethissite.com/pages/simple/
  # Queries to run
  # Each child query runs inside the parent
  queries:
    CountryEntry: # Query name
      # What to query for
      query: .country
      # Should we select all elements?
      # (querySelector or querySelectorAll)
      # Defaults to false
      all: true
      # JS function to evaluate the selected element(s)
      # Defaults to (e) => e.innerText
      eval: (e) => e.innerText
      # Python regex
      # If set, catches the first group with re.DOTALL enabled
      # Defaults to null
      regex: null
      # Result formatting
      # 'Hello my name is {}'.format(...)
      # Defaults to '{}'
      format: "{}"
      # Queries to run inside the selected element(s)
      # Defaults to null
      children:
        Country:
          query: .country-name
          # all: false
          # eval: (e) => e.innerText
          # regex: null
          # format: '{}'
          # children: null
        Info:
          query: .country-info
          # all: false
          eval: (e) => e.innerHTML
          # regex: null
          # format: '{}'
          # children: null
        Capital:
          query: .country-capital
          # all: false
          # eval: (e) => e.innerText
          # regex: null
          # format: '{}'
          # children: null
```

## Plugin system

You can add custom implementations by exposing 'cardscraper.x' entry point in
your package

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
