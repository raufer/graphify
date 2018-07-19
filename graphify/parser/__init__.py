from graphify.build.traverse import build
from graphify.descriptor.utils import compile_patterns
from graphify.models.document import Document


class Parser(object):
    """
    Generic Document Parser
    Needs a 'descriptor' that characterizes the different sections of the document
    """
    def __init__(self, descriptor):
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
