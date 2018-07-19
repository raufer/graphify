from itertools import chain


def filter_dfs(graph, predicate, source=None):
    """
    Search the 'graph' for nodes, whose data respects the 'predicate'
    Returns a generator of node keys, since we might just want the first hit

    Uses DFS for the graph traversal
    """
    source = source or graph.root_key

    it = (r for l, r in graph.dfs(source=source) if predicate(graph[r]))

    if predicate(graph[source]):
        it = chain.from_iterable([[source]] + [it])

    return it


def filter_bfs(graph, predicate, source=None):
    """
    Search the 'graph' for nodes, whose data respects the 'predicate'
    Returns a generator of node keys, since we might just want the first hit

    Uses BFS for the graph traversal
    """
    source = source or graph.root_key

    it = (r for l, r in graph.bfs(source=source) if predicate(graph[r]))

    if predicate(graph[source]):
        it = chain.from_iterable([[source]] + [it])

    return it


def filter_bfs_ancestors(graph, source, predicate):
    """
    Assumes a directed acyclic graph. Otherwise we cannot retrieve the 'parents' of a node and the recursive call would
    cause an overflow.

    Starting from 'source' go up in the hierarchy, using bfs and returns a generator of the nodes respecting 'predicated'
    """

    def loop(tovist):

        if not tovist or graph[tovist[0]].get('level', -1) == 0:
            return None

        elif predicate(graph[tovist[0]]):
            yield tovist[0]
            yield from loop(tovist[1:] + list(graph.parents(tovist[0])))

        else:
            yield from loop(tovist[1:] + list(graph.parents(tovist[0])))

    return loop(list(graph.parents(source)))
