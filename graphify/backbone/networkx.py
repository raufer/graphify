import networkx as nx

from graphify.backbone import GraphBackboneAbstraction


class NetworkxImplementation(GraphBackboneAbstraction):
    """
    Concrete implementation to serve a networkx backbone
    """

    def initialize(self):
        self.graph = nx.DiGraph()
        return self.graph

    def add_node(self, node, **data):
        self.graph.add_node(node, **data)

    def add_edge(self, a, b):
        self.graph.add_edge(a, b)

    def number_of_nodes(self):
        return nx.number_of_nodes(self.graph)

    def nodes(self):
        return list(self.graph.nodes())

    def edges(self, key=None):
        if not key:
            return list(self.graph.edges())
        else:
            return list(self.graph.edges(key))

    def exists_path(self, node_a, node_b):
        return nx.has_path(self.graph, node_a, node_b)

    def dfs(self, source=None):
        return nx.dfs_edges(self.graph, source=source or self.root_key)

    def bfs(self, source=None):
        return nx.bfs_edges(self.graph, source=source or self.root_key)

    def __getitem__(self, key):
        return self.graph.node[key]

if __name__ == '__main__':
    NetworkxImplementation()


