import logging

from graphify.build.traverse import build
from graphify.descriptor.utils import compile_patterns
from graphify.descriptor.utils import extend_internal_patterns
from graphify.descriptor.utils import extend_descriptor_with_data_capture_group
from graphify.models.document import Document

from functools import reduce
from typing import Iterable
from typing import Dict

from graphify.ops.document import map_values

logger = logging.getLogger(__name__)


class Parser(object):
    """
    Generic Document Parser
    Needs a 'descriptor' that characterizes the different sections of the document
    """
    def __init__(self, descriptor):
        self.descriptor = extend_internal_patterns(descriptor)
        self.descriptor = compile_patterns(descriptor)

    def parse(self, iterable) -> Document:
        """
        Given an iterable structure, parse them into a graph and return a 'Document' object
        """
        graph = build(iterable, self.descriptor)
        return Document(graph, "ROOT [0]")

    def parse_filepath(self, filepath) -> Document:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return self.parse(lines)


def parse_iterable(it: Iterable[str], descriptor: Dict, name: str = 'ROOT') -> Document:
    """
    Given a descriptor that describes the hierarchical structure of an iterable
    parse it into a graph representation

    'name' is the document name without spaces
    """
    descriptor = extend_internal_patterns(descriptor)
    descriptor = extend_descriptor_with_data_capture_group(descriptor)
    descriptor = compile_patterns(descriptor)

    graph = build(it, descriptor, name)
    document = Document(graph, "{} [0]".format(name))

    document = post_build_process(document, descriptor)
    return document


def parse_filepath(filepath: str, descriptor: Dict) -> Document:
    """
    Utility method to wrap `parse_iterable` with a file opening action
    """
    with open(filepath, "r", encoding="utf-8") as f:
        it = f.readlines()
        return parse_iterable(it, descriptor)


def post_build_process(document: Document, descriptor: Dict) -> Document:
    """
    After the base parsing process is complete it might be
    necessary to do some house keeping.

    The following operations are in scope:
        - Remove any internal tags from the 'content' data field of each node
          e.g. parsing hints like '[[Component]]'
    """
    def remove_occurrences(data):
        data['text'] = [
            reduce(lambda acc, x: x.sub('', acc), descriptor['exclude'], line)
            for line in data['text']
        ]
        return data

    document = map_values(document, remove_occurrences)
    return document
