
def handle_new_hit(graph, match, insert_level, last_node, descriptor):
    """
    Accommodate a new match into to the graph, possibly adding more than one node.
    If there is a gap between the depth of the node to add and the last inserted node
    we need to pad with dummy nodes (if configured) to enforce an uniform document structure

    There are three cases that need to be considered:
    - a node with a higher level was detected and padding is required
    - a node with a higher level was detected and padding is not required
    - every other case (same level or less)
    """

    current_level = graph[last_node]['level']

    if insert_level > current_level and descriptor['padding']:
        last_node = _pad(graph, last_node, current_level + 1, insert_level, descriptor)
        meta = descriptor['components'][insert_level - 1]
        _add_node(graph, meta, last_node, meta=meta, level=insert_level, pad=0)

    elif insert_level > current_level:
        meta = descriptor['components'][insert_level - 1]
        _add_node(graph, meta, last_node, meta=meta, level=insert_level)

    else:
        pass


def _add_node(graph, key, parent, **data):
    """
    Add a new node to the graph with the identifier 'key'. This key should be further enhanced with a unique identifier
    'data' should be a dictionary with the data to be held by the node

    Returns a key to the newly created node
    """
    #  TODO: 'parent' is assuming a direct graph and a single connection. This assumption is too much restrictive

    new_node = _build_node_key(key, graph.next_id())
    graph.add_node(new_node, **data)
    graph.add_edge(parent, new_node)
    return new_node


def _pad(graph, last_node, level, concrete_level, descriptor):
    """
    To introduction of padding nodes serves to keep the structure consistent
    We can be sure that, given a node belonging to level X, the full formal hierarchy from the root to X will be present
    The padding process continues until the current level is at X-1, where the non-padding node will be inserted

    Returns the identifier of the last inserted node
    """
    if level == concrete_level:
        return last_node
    else:
        meta = descriptor['components'][level - 1]
        node = _add_node(graph, meta, last_node, meta=meta, level=level, pad=1)
        return _pad(graph, node, level + 1, concrete_level, descriptor)


def _build_node_key(base, id):
    return '{} [{}]'.format(base, id)

