import networkx as nx

from unittest import TestCase

from graphify.backbone.networkx import NetworkxImplementation
from graphify.build.initialization import initialize_backbone


class TestBuildInitialization(TestCase):
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

    def test_initialize_graph(self):
        """
        A raw graph should be initialized with just one node, the root node 'ROOT [0]'. Its level should be set to 0
        The root node name should be customizable
        """
        graph = initialize_backbone(NetworkxImplementation())

        self.assertEqual(nx.number_of_nodes(graph), 1)
        self.assertListEqual(list(graph.nodes()), ['ROOT [0]'])
        self.assertEqual(graph['ROOT [0]']['level'], 0)
        self.assertEqual(graph['ROOT [0]']['meta'], 'root')






