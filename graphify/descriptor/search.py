

def search_descriptor_patterns(x, descriptor):
    """
    Given a descriptor object, traverse all of the patterns and check for a match
    If there is in fact a match, return the associated structural level of the match along with the match

    Assumes the list of patterns comes in ordered by the taxonomy hierarchy
    The level is returned with 1-based index since the level 0 is reserved for the root node
    """

    is_hit = lambda x, y: bool(x.search(y))
    search = lambda x, y: x.search(y)

    hit, level = next((
        (search(pattern, x), i+1)
        for i, pattern in enumerate(descriptor['patterns']) if is_hit(pattern, x)), (None, None)
    )

    return hit, level
