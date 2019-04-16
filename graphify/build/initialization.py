

def initialize_backbone(fw):
    """
    Initialize an raw Direct Graph and return it
    'ROOT [0]' is the identifier of the DiGraph root node, composing the only node present at level 0

    'fw' is the underlying graph framework used
    """
    base = fw.root
    key = fw.root_key
    meta = base.lower()

    fw.initialize()
    fw.add_node(key, meta=meta, level=0, text=[], pad=False, id=('/' + meta))

    return fw
