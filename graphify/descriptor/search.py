

def search_descriptor_patterns(x, descriptor):
    """
    Given a descriptor object, traverse all of the patterns and check for a match
    If there is in fact a match, return the associated structural level of the match along with the match

    Assumes the list of patterns comes in ordered by the taxonomy hierarchy
    The level is returned with 1-based index since the level 0 is reserved for the root node
    """

    def is_hit(x, y):
        return any((bool(i.search(y)) for i in x))

    def search(x, y):
        it = (i.search(y) for i in x)
        return next(i for i in it if bool(i))

    it = (
        (search(pattern, x), i + 1)
        for i, pattern in enumerate(descriptor['patterns']) if is_hit(pattern, x)
    )

    hit, level = next(it, (None, None))
    return hit, level
