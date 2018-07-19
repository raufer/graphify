from abc import ABC, abstractmethod


class GraphBackboneAbstraction(ABC):
    """
    Abstract class defining an interface that supports all of the
    primitive operations needed by graphify core

    Ultimately we might want to reuse the library with different backbones for the underlying graph framework
    The goal of this contract is to abstract the graph framework being used
    """

    def __init__(self):
        self._id = -1
        self.root = "ROOT"
        self.root_key = "{} [{}]".format(self.root, self.next_id())
        self.last_inserted = None
        self.graph = None

    @abstractmethod
    def initialize(self):
        """
        Raw graph initialization
        """
        pass

    @abstractmethod
    def add_node(self, node, *data):
        pass

    @abstractmethod
    def add_edge(self, a, b):
        pass

    @abstractmethod
    def number_of_nodes(self):
        pass

    @abstractmethod
    def nodes(self):
        """Returns a list of all of the nodes that compose the graph"""
        pass

    @abstractmethod
    def edges(self, key=None):
        """
        Returns a list of all of the edges associated with the node with identifier 'key'
        Otherwise returns a list of all of the edges present in the graph
        """
        pass

    @abstractmethod
    def parents(self, source):
        """
        Returns a generator with parents of 'source'. Assumes a directed graph
        """
        pass

    @abstractmethod
    def exists_path(self, a, b):
        """
        Returns a boolean indicating if there exists a path between nodes 'a' and 'b'
        The directionality (or lack of it) has a major impact.
        """
        pass

    @abstractmethod
    def dfs(self, source):
        """
        Traverse the graph structure reachable from 'source': depth first search
        Returns a generator of tuples (pairs od edges)
        """
        pass

    @abstractmethod
    def bfs(self, source):
        """
        Traverse the graph structure reachable from 'source': breath first search
        Returns a generator of tuples (pairs od edges)
        """
        pass

    def cursor(self):
        """
        Returns the last inserted node of the graph
        """
        return self.last_inserted

    def cursor_data(self, selector=None):
        """
        Returns the data belonging to the last inserted node
        If 'fields' is set return just a samller view of the content
        """
        if not selector:
            return self.__getitem__(self.cursor())

        elif isinstance(selector, list):
            data = self.__getitem__(self.cursor())
            return {f: data[f] for f in selector}

        else:
            return self.__getitem__(self.cursor())[selector]

    def next_id(self):
        self._id += 1
        return self._id

    @abstractmethod
    def __getitem__(self, key):
        """Access the data contained in a node"""
        pass


