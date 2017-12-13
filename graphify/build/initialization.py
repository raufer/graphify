

def initialize_backbone(fw, root_key=None):
    """
    Initialize an raw Direct Graph and return it
    'ROOT [0]' is the identifier of the DiGraph root node, composing the only node present at level 0

    'fw' is the underlying graph framework used
    """
    key = root_key or fw.root_key

    node = '{} [{}]'.format(key, fw.next_id())

    fw.initialize()
    fw.add_node(node, meta=key.lower(), level=0)

    return fw
