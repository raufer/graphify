
def filter_dfs(graph, predicate, source=None):
    """
    Search the 'graph' for nodes, whose data respects the 'predicate'
    Returns a generator of node keys, since we might just want the first hit

    Uses DFS for the graph traversal
    """
    return (r for l, r in graph.dfs(source=source) if predicate(graph[r]))


def filter_bfs(graph, predicate, source=None):
    """
    Search the 'graph' for nodes, whose data respects the 'predicate'
    Returns a generator of node keys, since we might just want the first hit

    Uses BFS for the graph traversal
    """
    return (r for l, r in graph.bfs(source=source) if predicate(graph[r]))
