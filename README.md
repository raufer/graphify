# Graphify

## Motivation

This library helps converting text documents with an inherent hierarchy into a graph that captures
that structure.

The following working pipeline is assumed:

```
[raw data] -> [lines of text] -> [graph]
```

## Basic Usage

In its most simple form, the usage is pretty simple:

```python
from graphify.parsing import parse_iterable

it = [
    "[[Chapter]] Chapter I",
    "This is chapter I text",
    "[[Article]] Article I",
    "This is article I text",
]

descriptor = {
    'components': ['Chapter', 'Article'],
    'patterns': ['Chapter', 'Article']
}

doc = parse_iterable(it, descriptor)
```

After having a list of lines that represent the text content of the document, we need to parse it into a graph.

Suppose we needed to capture the inherent graph structure of the following text (in list form).

(the text was deliberately altered to be more easy to parse)

```
Schedule 1 - GENERAL INVESTMENT GUIDELINES
  28
PPL – MAGIM FInal
PART 1- INVESTMENT RESTRICTIONS
The Manager must pay due regard to Applicable Laws and Regulations governing admissibility and permissibility of assets. The Manager may knowingly invest in assets which are impermissible only subject to the prior written approval of the Chief Actuary of the Client.
Derivatives will be used only in a manner consistent with the usage restrictions described in the Applicable Laws and Regulations.
1. General Restrictions
1.1 The basic restrictions applicable to the Assets are specified in the PRA and/or FCA's Permitted Links Rules in its Conduct of Business Sourcebook (COBS). and the Prudential Sourcebook for Insurers (INSPRU).
1.2. The Client has determined that such basic restrictions, specified in paragraph 1 above, should be supplemented by:
1.2.1 the general terms contained within this Agreement; and
1.2.2 detailed restrictions specified in this Schedule 1 or in the relevant portion of Schedule 2
1.3 There shall be no negative currency exposures other than in relation to the Funds specified in paragraph 2.2.1 below but always subject to any constraints contained in Paragraph 1.1 of this Schedule.
2. Derivative Restrictions
2.1 Specific restrictions
2.1.1 Permitted exchanges and contracts
Instruments must be listed(1) or with an approved counterparty(1) and must be capable of being readily
closed out at a price the basis of which is pre-determined.
Any exchange traded derivative that qualifies as a permitted link shall be allowed for efficient portfolio management purposes within any PPL Fund.
In addition, the Manager may purchase and sell listed Warrants.
2.1.2 Counterparty Restrictions
Forward Currency Contracts are restricted to those transacted with banks identified on the “Approved Bank Counterparties” list maintained by the Manager’s Treasury. A copy of this list can be made available to the Client on request. Refer to Schedule 2 for fund specific restrictions. In the event of any conflict between the terms of Schedule 1 and Schedule 2, the terms of the latter shall prevail.
```

The parser, in its most simple form, will need a `descriptor` that describes the hierarchical structure of the document along with a regex (can be customized to use a custom function) to detect each component.

```python
from graphify.parsing import parse_iterable

text = [...]


descriptor = {
    'components': ['Schedule', 'Part', 'Section', 'Point', 'Subpoint'],
    'patterns': [r'^Schedule\s\d{1,2}', r'^PART\s\d{1,2}', r'^\d{1,2}\.\s', r'^\d{1,2}\.\d{1,2}\.\s', r'^\d{1,2}\.\d{1,2}\.\d{1,2}\s']
}

doc = parse_iterable(text, descriptor)
```

Which will result in the following structure
```
Schedule 1
        PART 1
                1.
                        1.1.
                        1.2.
                                1.2.1
                                1.2.2
                        1.3.
                2.
                        2.1.
                                2.1.1
                                2.1.2

```

The descriptor can be customized with other logic, e.g.:

```python
descriptor = {
    'components': ['Section', 'Subsection'],
    'patterns': [r'^\d{1,2}[A-Z]?\.?\s', r'^\d{1,2}[A-Z]?\.\d{1,2}\s'],
    'stopParsing': r'^Annex',
    'startParsing': r'the provisions of any'
}
```

Gives indication of signals to start/stop the parsing.

Additionally we can set a flag indicating if we need a "padded" structure, i.e. if dummy nodes should be create to enforce a constant structure. For instance, if the document goes from a `Part` directly to a `Article`, without mentioning a `Chapter` (which could be an intermediary structure expected), and the 
flag is set to true, the parser creates a dummy node `Chapter 0` with no content just to ensure the structure.

```python
descriptor = {
    'components': ['Section', 'Subsection'],
    'patterns': [r'^\d{1,2}[A-Z]?\.?\s', r'^\d{1,2}[A-Z]?\.\d{1,2}\s'],
    'padding': True
}
```

If more complex logic is needed the parser can be customized.

### Descriptor

So the general form of the patterns is the following:

```python
descriptor = {
    'components': ['Section', 'Subsection'],
    'patterns': [r'^\d{1,2}[A-Z]?\.?\s', r'^\d{1,2}[A-Z]?\.\d{1,2}\s']
}
```

However, if the tags are artificially controlled by us, e.g. by inserting them into the text (lets take the ``[[`` as the de facto way of artifically inserting tags)

```python
it = [
    "[[Chapter]] Chapter I",
    "This is chapter I text",
    "[[Article]] Article I",
    "This is article I text",
]
```

Then you can use a sortcut in the `patterns` fields, i.e.

```python
descriptor = {
    'components': ['Chapter', 'Article'],
    'patterns': ['Chapter', 'Article']
}
```

Instead of

```python
descriptor = {
    'components': ['Chapter', 'Article'],
    'patterns': ['[[Chapter]]', '[[Article]]']
}
```

Additionally the parsing will get rid of the tags and take care of the extra spaces in the cases that the `pattern` is followed by a space, e.g. `[[Chapter]] Chapter I` -> ``Chapter I``


### Advanced Usage

For some situations we might require to inject custom data into the parsing process; this comes in contrast to `grapfiphy` being responsible for creating the metadata that supports these documents. For example 
we might be parsing a document that contains a valid URI for each section of the document. In these cases we might prefer to use these instead if relying on `grafiphy` to create new ones.

```python
it = [
    "[[Chapter]]{'id': '/base/chapter/1'} Chapter I",
    "This is chapter I text",
    "[[Article]]{'id': '/base/article/1'} Article I",
    "This is article I text",
]

descriptor = {
    'components': ['Chapter', 'Section', 'Sub-section', 'Article'],
    'patterns': ['Chapter', 'Section', 'Sub-section', 'Article']
}

doc = parse_iterable(it, descriptor)
```

This would result in two nodes, `Chapter` and `Article`, with custom node `ids`:

```python
result = [n for n in doc.graph.nodes(data=True)]

expected = [
    ('ROOT [0]', {'meta': 'root', 'level': 0, 'text': [], 'pad': False, 'id': '/root'}),
    ('Chapter [1]', {'meta': 'Chapter', 'level': 1, 'pad': False, 'text': ["Chapter I", 'This is chapter I text'], 'id': '/base/chapter/1'}),
    ('Article [2]', {'meta': 'Article', 'level': 4, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/base/article/1'})
]
```


#### Metadata

Different documents coming from different sources might have different metadata requirements; In order
to not have to make any assumptions in `grafiphy` or introduce a awkward API to describe metadata, we suggest
that this is done as an intermediary step:

```python

from graphify.parsing import parse_iterable

it = [
    "[[Chapter]] Chapter I",
    "This is chapter I text",
    "[[Article]] Article I",
    "This is article I text",
]

descriptor = {
    'components': ['Chapter', 'Article'],
    'patterns': ['Chapter', 'Article']
}

doc = parse_iterable(it, descriptor)

metadata = {
    'title': 'A',
    'year': 2000,
    'industry': 'finance'
}

doc = {**doc.to_dict(), **metadata}
```


