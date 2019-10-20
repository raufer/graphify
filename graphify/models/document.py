import re
import logging
import networkx as nx

from nxpd import draw

from graphify.backbone.networkx import NetworkxImplementation
from graphify.utils.recipes import flatten

logger = logging.getLogger(__name__)


class Document(object):
    """
    Document representation providing useful functions to extract information from documents
    conversion to json representation is also available
    """

    def __init__(self, graph, root):
        self.graph = graph
        self.root = root
        self.active_depth = None
        self.max_depth = None
        self.set_depths()

    def id(self):
        return self.graph.node[self.root]["id"]

    def id_ending_with(self, suffix):
        """
        Returns a tuple (key, data) for a the whose ID ends with the token 'suffix'
        eg. id_ends_with('chapter-xii') -> 'document-a/title-vii/chapter-xii' (first match) (and should be only)
        """
        node = [(key, data) for key, data in self.traverse() if data['id'].endswith(suffix)]
        if node:
            return node[0]

    def draw(self):
        """plot the graph to help visualisation"""
        draw(self.graph)

    def to_dict(self):
        """
        parsing from nx graph representation to dict/json
        """
        result = {"document_name": self.root_node()["meta"], "nodes": []}
        for node, data in self.traverse():
            successors = list(self.successors(node))
            predecessors = list(self.predecessors(node))
            result["nodes"].append(
                {"key": node, "content": data, "successors": successors, "predecessors": predecessors})
        return result

    @staticmethod
    def from_dict(d):
        root_node = d["nodes"][0]

        graph = NetworkxImplementation(root_node['key'].split(' ')[0])
        graph.initialize()

        # add nodes first
        for node_all_data in d["nodes"]:
            node_key = node_all_data["key"]
            graph.add_node(node_key, attr_dict=node_all_data["content"])

        # add edges
        for node_all_data in d["nodes"]:
            key = node_all_data["key"]
            graph.add_edges_from(map(lambda p: (p, key), node_all_data["predecessors"]))
            graph.add_edges_from(map(lambda s: (key, s), node_all_data["successors"]))

        doc = Document(graph, root_node['key'])

        return doc

    def set_depths(self):
        self.active_depth = self._active_depth()
        self.max_depth = self._max_depth()

    def node(self, key):
        return self.graph.node[key]

    def nodes(self, depth, node_data=True):
        for node, data in self.graph.nodes_iter(data=True):
            if data['level'] == depth and not node_data:
                yield node
            elif data['level'] == depth and node_data:
                yield (node, data)

    def search(self, pattern):
        """search for nodes whose 'meta' match a given pattern"""
        result = None
        for node, data in self.traverse():
            if pattern in data['meta']:
                return node, data
        return result

    def search_by_pattern(self, pattern, key=lambda data: data['meta']):
        """
        Searches for nodes whose 'meta' match a given pattern.
        Whitespaces in the pattern are ignored. To include whitespaces, use '\s'
        """
        result = []
        for node, data in self.traverse():
            if re.search(pattern, key(data), flags=re.VERBOSE):
                result.append([node, data])
        return result

    def root_node(self, data=True):
        """
        return roots node: just key or dict with data, depending on the data flag
        """
        if data:
            return self.graph.node[self.root]
        else:
            return self.root

    def text(self, just_text=False):
        """
        get all of the ordered text lines composing the document
        the resulting text should keep intact the structure of the source
        """
        lines = []
        for node, data in self.traverse():
            if just_text or data['has_text'] or data['pad']:
                lines += data['text']
            else:
                lines += [data['meta']] + data['title'] + data['text']
        return flatten(lines)

    def traverse(self, data=True):
        """
        returns a generator with the nodes ordered by the time of insertion
        """
        nodes = sorted(self.graph.nodes(), key=lambda x: key_to_numeric(x))
        for node in nodes:
            yield (node, self.graph.node[node]) if data else node

    def leaf_nodes(self, data=True):
        """
        Return all leaf nodes of the graph
        Note that this does not necessarily mean that they will all be paragraphs
        We're returning all the nodes that do not have predecessors in the direct graph
        """
        leaf_nodes = [
            node for node in self.graph.nodes()
            if self.graph.in_degree(node) != 0 and self.graph.out_degree(node) == 0
        ]
        for node in leaf_nodes:
            yield (node, self.graph.node[node]) if data else node

    def paragraphs(self, data=True):
        """
        Return all paragraphs of the graph
        These are the ones which have the depth equal to 'max_depth' as detected in the construction of the Doc
        """
        return self.nodes(self.max_depth, data)

    @staticmethod
    def identifier(x):
        reg = re.compile(r'\[(\d+\_?(\d+)?)[a-z]?\]')
        return reg.search(x).groups(0)[0]

    def _max_depth(self):
        """
        get maximum depth of the graph
        """
        max_depth = 0
        for node, data in self.traverse():
            max_depth = max(max_depth, data['level'])
        return max_depth

    def _active_depth(self):
        """
        get first level that is actual populated by content (i.e. is not a padding node)
        """
        for n_left, n_right in self.graph.dfs():
            if self.node(n_right)['pad'] == 0:
                return self.node(n_right)['level']
        return 0

    def get_level(self):
        """returns the level of the document. returns None if the document does not have the level field"""
        try:
            return self.root_node()['document_level']
        except KeyError:
            return None

    def append_references_for_level(self, node_key, level, ref, ref_key='references'):
        """
        adds to 'ref' to the list of 'level' from node with 'node_key'.
        if level is None, 'ref' is added to 'unknown' field
        """
        if level:
            level_key = "level_{}".format(level)
            self.node(node_key)[ref_key][level_key].append(ref)
        else:
            # unknown level references
            self.node(node_key)[ref_key]['unknown'].append(ref)
        return self

    def successors(self, node):
        return self.graph.successors(node)

    def predecessors(self, node):
        return self.graph.predecessors(node)

    def flat_report(self, consider_leafs=False):
        """
        simple verification report that gives that count of occurrences of each level of the given structure
        e.g
            level 1 (e.g. Parts): 2,
            ...
            level 6 (e.g. paragraphs): 20

        consider_leafs is a flag to include the leafs in the report or not
        usually their number is huge and hard to manually confirm
        """
        report = {}
        for node, data in self.traverse():
            if data['pad'] or (data['level'] == self.max_depth and not consider_leafs):
                continue
            elif int(data['level']) not in report:
                report[int(data['level'])] = 1
            else:
                report[int(data['level'])] += 1
        return report

    def __getitem__(self, key):
        return self.graph.node[key]

    def __setitem__(self, key, value):
        self.graph.node[key] = value

    def __repr__(self):
        """Useful document representation"""
        repr = ''
        acc = 0
        for node, data in reversed(list(self.traverse())):
            if not data['pad']:
                offset = '\t' * (data['level'] - self.active_depth)
                if 'has_text' in data and data['has_text'] == 1:
                    acc += 1
                else:
                    repr += '{}{}{}\n'.format(offset, data['meta'], '[{}]'.format(str(acc)) if acc else '')
                    acc = 0
        repr_lines = reversed(repr.split('\n'))
        repr = '\n'.join(repr_lines)
        return repr

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


def _merge_accumulator(acc, new_acc):
    """
    merge accumulators elements that are of the same type
    e.g.:
        [[A], [A], [B]] => [[A,A], [B]]
    """
    if not acc:
        return new_acc

    if not new_acc:
        new_acc.append(acc[0])
        return _merge_accumulator(acc[1:], new_acc)

    elif acc[0][0]['level'] == new_acc[-1][-1]['level']:
        new_acc[-1] += acc[0]
        return _merge_accumulator(acc[1:], new_acc)

    else:
        new_acc.append(acc[0])
        return _merge_accumulator(acc[1:], new_acc)


def key_to_numeric(x):
    """
    Represent a node identifier (key) by a numeric value to be used in the representation
    Useful to sorting operations
    """
    reg = re.compile(r'\[(\d+\_?(\d+)?)[a-z]?\]')
    inspect = reg.search(x).groups(0)[0]
    if '_' in inspect:
        left, right = inspect.split('_')
        return int(left), int(right)
    else:
        return int(inspect), 0
