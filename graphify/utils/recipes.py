import collections
import operator

from functools import reduce
from collections import MutableMapping
from itertools import chain, islice


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def consume(iterator, n=None):
    """
    Advance the iterator n-steps ahead. If n is none, consume entirely.
    Use functions that consume iterators at C speed.
    """
    if n is None:
        # feed the entire iterator into a one length deque
        last = collections.deque(iterator, maxlen=1)
        return last.pop() if last else None
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def explode(iterable, f, g=operator.itemgetter(0)):
    """
    'explode(it, f)' should take a iterable 'it :: [a]' and two functions 'f' and 'g'
    'f :: a -> [b]' chooses the elements to explode
    'g :: a -> b' picks the constant element to be paired with each 'b'
    'f' is applied to every element of 'it' and a new entry '(a, b)' is added to for every 'b' in '[b]'
    >>> a = [ (0, ['A', 'B', 'C']), (1, ['D']) ]
    >>> explode(it, lambda x: operator.itemgetter(1))
    >>> [(0, 'A'), (0, 'B'), (0, 'C'), (1, 'D')]
    """
    return flatten(((g(i), j) for j in f(i)) for i in iterable)


def _compose2(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*fs):
    """"Returns composition of functions"""
    return reduce(_compose2, fs)


def group_by(f, seq):
    """
    Groups given sequence items into a mapping f(item) -> [item, ...].
    >>> a = [("A", 0, 1), ("B", 1, 1), ("A", 2, 2)]
    >>> group_by(a, lambda x: operator.itemgetter(1))
    >>> {"A": [("A", 0, 1), ("A", 2, 2)], "B": [("B", 1, 1)]}
    """
    result = collections.defaultdict(list)
    for item in seq:
        result[f(item)].append(item)
    return result


def _rec_merge(d1, d2):
    """
    Update two dicts of dicts recursively,
    if either mapping has leaves that are non-dicts,
    the second's leaf overwrites the first's.
    """
    for k, v in d1.items():
        if k in d2:
            if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                d2[k] = _rec_merge(v, d2[k])
    d3 = d1.copy()
    d3.update(d2)
    return d3


def merge_dicts(dicts):
    """
    Reduces a variable number of dicts into a single dict
    >>> dict1 = {1:{"a":'A'}, 2:{"b":'B'}}
    >>> dict2 = {2:{"c":'C'}, 3:{"d":'D'}}
    >>> merge_dicts([dict1, dict2])
    >>> {1: {'a': 'A'}, 2: {'c': 'C', 'b': 'B'}, 3: {'d': 'D'}}
    """
    return reduce(_rec_merge, dicts, {})

