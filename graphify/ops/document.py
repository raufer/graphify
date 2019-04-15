from graphify.models.document import Document
from typing import Callable
from typing import Dict
from operator import itemgetter


def copy(document: Document) -> Document:
    """
    Creates a deep copy of a given document
    """
    new_document = Document(document.graph.copy(), document.root)
    return new_document


def map_values(doc: Document, f: Callable[[Dict], Dict]) -> Document:
    """
    Map data receives a document and a function 'f' that operates on the data
    of each node, f :: {a, b} -> {c, d}
    Returns a new document object
    """
    doc = copy(doc)
    it = map(itemgetter(0), doc.traverse())

    for node in it:
        f(doc.graph[node])

    return doc

