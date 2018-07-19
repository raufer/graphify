import re

from unittest import TestCase

from graphify.backbone.networkx import NetworkxImplementation
from graphify.build.initialization import initialize_backbone
from graphify.build.graph import _add_node, _pad, handle_match
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

    def test_handle_match_next_in_the_hierarchy(self):
        """
        When traversing the input, if a new match is encountered, it should be properly accommodated on the graph.
        In the most simple case, we detect a node that follows next on the hierarchy
        """
        match = re.compile(r'Test Match').search('This is a Test Match sentence')

        descriptor = {
            'components': ['A', 'B', 'C', 'D'],
            'patterns': [r'A', r'B', r'C', r'D'],
            'padding': True
        }

        descriptor = compile_patterns(descriptor)

        graph = initialize_backbone(NetworkxImplementation())

        inserted = handle_match(graph, match, 1, descriptor)

        self.assertEqual(inserted, "Test Match [1]")
        self.assertListEqual(sorted(graph.nodes()), sorted(["ROOT [0]", "Test Match [1]"]))
        self.assertDictEqual(graph["Test Match [1]"], {'pad': 0, 'meta': 'Test Match', 'level': 1, 'content': []})

    def test_handle_match_next_in_the_hierarchy_requiring_padding(self):
        """
        When traversing the input, if a new match is encountered, it should be properly accommodated on the graph.
        If the new level does not immediately follows the next on the hierarchy, and if padding is set to True
        then we need to pad additional nodes
        """
        match = re.compile(r'Test Match').search('This is a Test Match sentence')

        descriptor = {
            'components': ['A', 'B', 'C', 'D'],
            'patterns': [r'A', r'B', r'C', r'D'],
            'padding': True
        }

        descriptor = compile_patterns(descriptor)

        graph = initialize_backbone(NetworkxImplementation())

        inserted = handle_match(graph, match, 3, descriptor)

        self.assertEqual(inserted, "Test Match [3]")
        self.assertListEqual(sorted(graph.nodes()), sorted(["ROOT [0]", "Test Match [3]", "A [1]", "B [2]"]))
        self.assertDictEqual(graph["A [1]"], {'pad': 1, 'meta': 'A', 'level': 1, 'content': []})
        self.assertDictEqual(graph["B [2]"], {'pad': 1, 'meta': 'B', 'level': 2, 'content': []})
        self.assertDictEqual(graph["Test Match [3]"], {'pad': 0, 'meta': 'Test Match', 'level': 3, 'content': []})

    def test_handle_match_next_in_the_hierarchy_requiring_padding_set_to_false(self):
        """
        When traversing the input, if a new match is encountered, it should be properly accommodated on the graph.
        If the new level does not immediately follows the next on the hierarchy, and if padding is set to False
        then we just ignore the gap between the levels
        """
        match = re.compile(r'Test Match').search('This is a Test Match sentence')

        descriptor = {
            'components': ['A', 'B', 'C', 'D'],
            'patterns': [r'A', r'B', r'C', r'D'],
            'padding': False
        }

        descriptor = compile_patterns(descriptor)

        graph = initialize_backbone(NetworkxImplementation())

        inserted = handle_match(graph, match, 3, descriptor)

        self.assertEqual(inserted, "Test Match [1]")
        self.assertListEqual(sorted(graph.nodes()), sorted(["ROOT [0]", "Test Match [1]"]))
        self.assertDictEqual(graph["Test Match [1]"], {'pad': 0, 'meta': 'Test Match', 'level': 3, 'content': []})

    def test_handle_match_higher_on_the_hierarchy(self):
        """
        When traversing the input, if a new match is encountered, it should be properly accommodated on the graph.
        If the new level precedes the current one, we should find the appropriate parent to accommodate this new node
        and properly insert it
        """
        match = re.compile(r'Test Match').search('This is a Test Match sentence')

        descriptor = {
            'components': ['A', 'B', 'C', 'D'],
            'patterns': [r'A', r'B', r'C', r'D'],
            'padding': False
        }

        descriptor = compile_patterns(descriptor)

        graph = initialize_backbone(NetworkxImplementation())

        _ = handle_match(graph, match, 1, descriptor)

        _ = handle_match(graph, match, 2, descriptor)

        inserted = handle_match(graph, match, 1, descriptor)

        self.assertEqual(inserted, "Test Match [3]")
        self.assertListEqual(sorted(graph.nodes()), sorted(["ROOT [0]", "Test Match [1]", "Test Match [2]", "Test Match [3]"]))
        self.assertDictEqual(graph["Test Match [3]"], {'pad': 0, 'meta': 'Test Match', 'level': 1, 'content': []})

        self.assertEqual(sorted([r for _, r in graph.edges("ROOT [0]")]), sorted(['Test Match [3]', 'Test Match [1]']))









