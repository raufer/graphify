from unittest import TestCase

from graphify.backbone.networkx import NetworkxImplementation
from graphify.build.initialization import initialize_backbone
from graphify.build.graph import _add_node, append_content


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

    def test_append_content(self):
        """
        Every line should be inserted as content of the node currently in focus
        """

        graph = initialize_backbone(NetworkxImplementation())

        graph = append_content(graph, "this is a sample line")

        self.assertEqual(graph.cursor_data('content'), ["this is a sample line"])

        data = {'level': 1, 'meta': 'ART', 'content': []}
        key = 'NEW NODE'
        parent = "ROOT [0]"

        _ = _add_node(graph, key, parent, **data)

        graph = append_content(graph, "yet another sample")
        graph = append_content(graph, "yet another sample 2")

        self.assertEqual(graph.cursor_data('content'), ["yet another sample", "yet another sample 2"])
