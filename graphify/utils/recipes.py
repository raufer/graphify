from inspect import signature


def arity_of(f):
    """Returns the number of arguments expected by callable 'f'"""
    return len(signature(f).parameters)


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)


def group_by_overlap(l):
    """
    Given a list of 'l' of tuples (a,b) group all the overlapping tuples, where the criteria is range(a,b)
    Assumes the elements are of integer type
    """
    tupled = [((a, b), range(a, b+1), False) for a, b in l]

    groups = []
    for a, b in l:
        span_range = range(a, b)
        group = []

        for i, it in enumerate(tupled):
            l, other_span_range, used = it
            if set(span_range).intersection(set(other_span_range)) and not used:
                group.append(l)
                tupled[i] = (l, other_span_range, True)

        groups.append(group)

    groups = [g for g in groups if g]

    return groups


