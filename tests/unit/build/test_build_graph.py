
from unittest import TestCase

from graphify.backbone.networkx import NetworkxImplementation
from graphify.build.initialization import initialize_backbone
from graphify.build.graph import _add_node, _pad
from graphify.descriptor.utils import compile_patterns


class TestBuildGraph(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_node(self):
        """
        We should be able to add a node to the graph with a dictionary with data to be held by the newly created node
        """

        graph = initialize_backbone(NetworkxImplementation())

        data = {'a': 1, 'b': 2}
        key = 'NEW NODE'
        parent = "ROOT [0]"
        new_node = _add_node(graph, key, parent, **data)

        self.assertEqual(new_node, "NEW NODE [1]")
        self.assertDictEqual(graph[new_node], data)
        self.assertEqual(graph.edges(parent), [('ROOT [0]', 'NEW NODE [1]')])

        data = {}
        key = 'NEW NODE'
        parent = "ROOT [0]"
        new_node = _add_node(graph, key, parent, **data)

        self.assertEqual(new_node, "NEW NODE [2]")
        self.assertDictEqual(graph[new_node], data)
        self.assertEqual(sorted(graph.edges(parent)), sorted([('ROOT [0]', 'NEW NODE [1]'), ('ROOT [0]', 'NEW NODE [2]')]))

    def test_padding_01(self):
        """
        When requested, the insertion of a new node must be preceded of a padding process which ensures an uniform and predictable hierarchy
        """
        descriptor = {
            'components': ['A', 'B', 'C', 'D'],
            'patterns': [r'A', r'B', r'C', r'D']
        }

        descriptor = compile_patterns(descriptor)

        graph = initialize_backbone(NetworkxImplementation())

        data = {'level': 1, 'meta': 'ART'}
        key = 'NEW NODE'
        parent = "ROOT [0]"
        node = _add_node(graph, key, parent, **data)

        last_node = _pad(graph, node, data['level']+1, 4, descriptor)

        self.assertListEqual(sorted(graph.nodes()), sorted(['ROOT [0]', 'NEW NODE [1]', 'B [2]', 'C [3]']))

        self.assertEqual(last_node, 'C [3]')

    def test_padding_no_effect(self):
        """
        If the requested level is just one below the hierarchy the padding process should leave the graph unchanged
        """
        descriptor = {
            'components': ['A', 'B', 'C', 'D'],
            'patterns': [r'A', r'B', r'C', r'D']
        }

        descriptor = compile_patterns(descriptor)

        graph = initialize_backbone(NetworkxImplementation())

        data = {'level': 1, 'meta': 'ART'}
        key = 'NEW NODE'
        parent = "ROOT [0]"
        node = _add_node(graph, key, parent, **data)

        nodes_before = sorted(graph.nodes())
        last_node = _pad(graph, node, 3 + 1, 4, descriptor)
        nodes_after = sorted(graph.nodes())

        self.assertEqual(last_node, node)
        self.assertListEqual(nodes_before, nodes_after)








