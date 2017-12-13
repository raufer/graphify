import logging
import networkx as nx

from graphify.build.initialization import initialize_graph
from graphify.descriptor.search import search_descriptor_patterns

logger = logging.getLogger(__name__)


def build(it, descriptor):
    """
    Initialize the empty raw graph and parse the iterable structure 'it'
    """
    graph = initialize_graph()

    graph = _iterative_traverse(it, graph, "ROOT [0]", descriptor)

    logger.debug("Raw graph constructed with '{0}' nodes".format(nx.number_of_nodes(graph)))


def _recursive_traverse(iterable, graph, last_node):
    """
    loop through the lines in a recursive manner
    at each iteration check to see if the current line indicates a need for:
        -stopping the capture (end of file)
    """

    if not iterable or self._finish_parsing(iterable[0]):
        return graph

    current_level = graph.node[last_node]['level']

    valid_element_level = self._get_level_if_valid_element(iterable[0])

    if valid_element_level:
        graph, last_node = self._add_node(graph, iterable[0], valid_element_level, current_level, last_node)

    self._add_text(graph.node[last_node]['text'], iterable[0], graph.node[last_node]['level'])

    return self._recursive_traverse(iterable[1:], graph, last_node)


def _iterative_traverse(iterable, graph, last_node, descriptor):
    """
    Loop through the lines in an iterative way

    This is necessary due to the lack of support of python to handle massive recursion

    At each iteration check to see if the current line triggers a signal to top the parsing process
    """
    for line in iterable:

        if descriptor['finishParsing'](line):
            break

        current_level = graph.node[last_node]['level']

        match, level = search_descriptor_patterns(line, descriptor)

        if match:
            graph, last_node = _add_node(graph, match, level, current_level, last_node)

        _add_text(graph.node[last_node]['text'], line, graph.node[last_node]['level'])

    return graph


