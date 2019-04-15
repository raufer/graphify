import logging
import networkx as nx

from itertools import dropwhile

from graphify.backbone.initialization import initialize_graph
from graphify.build.graph import handle_match, append_content
from graphify.descriptor.search import search_descriptor_patterns
from graphify.descriptor.utils import normalize_descriptor

logger = logging.getLogger(__name__)


def build(it, descriptor):
    """
    Initialize the empty raw graph and parse the iterable structure 'it'
    """
    graph = initialize_graph()

    descriptor = normalize_descriptor(descriptor)

    it = dropwhile(descriptor['startParsing'], it)

    graph = _iterative_traverse(it, graph, "ROOT [0]", descriptor)

    logger.info("Raw graph constructed with '{0}' nodes".format(nx.number_of_nodes(graph)))

    return graph


def _iterative_traverse(iterator, graph, last_node, descriptor):
    """
    Loop through the lines in an iterative way
    This is necessary due to the lack of support of python to handle massive recursion

    At each iteration check to see if the current line triggers a signal to top the parsing process
    """
    for line in iterator:

        if descriptor['stopParsing'](line):
            break

        match, level = search_descriptor_patterns(line, descriptor)

        if match:
            _ = handle_match(graph, match, level, descriptor)

        graph = append_content(graph, line)

    return graph


