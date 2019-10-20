import networkx as nx

from graphify.backbone import GraphBackboneAbstraction


class NetworkxImplementation(GraphBackboneAbstraction):
    """
    Concrete implementation to serve a networkx backbone
    """

    def initialize(self):
        self.graph = nx.DiGraph()
        return self.graph

    @property
    def node(self):
        return self.graph.node

    def add_node(self, node, **data):
        self.graph.add_node(node, **data)
        self.last_inserted = node

    def add_edge(self, a, b):
        self.graph.add_edge(a, b)

    def add_edges_from(self, it):
        self.graph.add_edges_from(it)

    def number_of_nodes(self):
        return nx.number_of_nodes(self.graph)

    def nodes(self):
        return list(self.graph.nodes())

    def nodes_iter(self, data=False):
        return self.graph.nodes(data=data)

    def edges(self, key=None):
        if not key:
            return list(self.graph.edges())
        else:
            return list(self.graph.edges(key))

    def parents(self, source):
        return self.graph.predecessors(source)

    def predecessors(self, source):
        return self.parents(source)

    def successors(self, source):
        return self.graph.successors(source)

    def exists_path(self, node_a, node_b):
        return nx.has_path(self.graph, node_a, node_b)

    def dfs(self, source=None):
        return nx.dfs_edges(self.graph, source=source or self.root_key)

    def bfs(self, source=None):
        return nx.bfs_edges(self.graph, source=source or self.root_key)

    def copy(self):
        g = NetworkxImplementation(self.root)
        g.graph = self.graph.copy()
        g.last_inserted = str(self.last_inserted)
        return g

    def __getitem__(self, key):
        return self.graph.node[key]


if __name__ == '__main__':
    NetworkxImplementation()


