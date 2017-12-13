
from unittest import TestCase

from graphify.backbone.networkx import NetworkxImplementation
from graphify.build.initialization import initialize_backbone
from graphify.build.graph import _add_node
from graphify.descriptor.utils import compile_patterns
from graphify.ops.search import filter_dfs, filter_bfs


class TestOpsSearch(TestCase):
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

    def test_search(self):
        """
        Filtering the nodes, reachable from a given source, should be possible by passing a predicate.
        """

        graph = initialize_backbone(NetworkxImplementation())

        parent = graph.root_key
        base = "NODE"
        for i in range(1, 10):
            parent = _add_node(graph, base, parent, tag=i)

        result = list(filter_dfs(graph, predicate=lambda x: x['tag'] == 5))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'NODE [6]')

        result = list(filter_dfs(graph, predicate=lambda x: x['tag'] == 5, source="NODE [7]"))

        self.assertEqual(len(result), 0)

    def test_search_dfs_bfs(self):
        """
        The complete result should not change depending on the traversal algorithm. The first match should however.
        """

        graph = initialize_backbone(NetworkxImplementation())

        root = graph.root_key
        base = "NODE"

        node_1 = _add_node(graph, base, root, tag=1)
        node_2 = _add_node(graph, base, root, tag=2)
        node_3 = _add_node(graph, base, node_2, tag=100)
        node_4 = _add_node(graph, base, node_1, tag=4)
        node_5 = _add_node(graph, base, node_2, tag=5)
        node_6 = _add_node(graph, base, node_1, tag=6)
        node_7 = _add_node(graph, base, node_4, tag=100)
        node_8 = _add_node(graph, base, node_4, tag=8)

        result_dfs = sorted(list(filter_dfs(graph, predicate=lambda x: x['tag'] == 100)))
        result_bfs = sorted(list(filter_bfs(graph, predicate=lambda x: x['tag'] == 100)))

        self.assertEqual(result_bfs, result_dfs)

        self.assertEqual(len(result_dfs), 2)
        self.assertListEqual(result_dfs, sorted(['NODE [4]', 'NODE [8]']))

        first_bfs = next(filter_bfs(graph, predicate=lambda x: x['tag'] == 100))
        first_dfs = next(filter_dfs(graph, predicate=lambda x: x['tag'] == 100))

        self.assertEqual(first_bfs, "NODE [4]")
        self.assertIn(first_dfs, ["NODE [8]", "NODE [4]"])











