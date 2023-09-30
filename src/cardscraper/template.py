TEMPLATE = """meta:
    package: default
    deck: default
    model: default
    scraping: default

package:
    name: Package
    output_path: ./out/
    media: null

deck:
    name: Deck
    id: # PUT ID HERE

model:
    name: Model 
    id: # PUT ID HERE
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
    templates:
        Card:
            qfmt: |
                <div class='question'>
                {{Question}}
                </div>
            afmt: |
                {{FrontSide}}
                <hr id='answer'>
                <div class='answer'>
                {{Answer}}
                </div>

scraping:
    urls:
        - # PUT AT LEAST ONE URL HERE
        # - URL 2
        # - etc
    queries:
        Entry:
            query: .entry
            all: true
            children:
                Question:
                    query: .question
                Answer:
                    query: .answer"""
