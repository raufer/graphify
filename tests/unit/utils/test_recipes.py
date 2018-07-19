import unittest
from operator import itemgetter

from graphify.utils.recipes import explode, merge_dicts


class TestRecipes(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_explode(self):
        """
        'explode(it, f)' should take a iterable 'it :: [a]' and a function 'f :: a -> [b]'
        'f' is applied to every element of 'it' and a new entry '(a, b)' is added to for every 'b' in '[b]'
        """

        #  consistency check
        self.assertListEqual(list(explode([], lambda x: [])), [])

        a = [
            (0, ["A", "B", "C"]),
            (1, ["D"]),
            (2, ["E", "F"])
        ]

        expected = [
            (0, "A"),
            (0, "B"),
            (0, "C"),
            (1, "D"),
            (2, "E"),
            (2, "F")
        ]

        self.assertListEqual(list(explode(a, itemgetter(1))), expected)

    def test_explode_empty_explosion_selection(self):
        """
        'explode(it, f)' should filter entries whose explosion picker 'f' results in an empty iterable
       """
        a = [
            (0, ["A", "B", "C"]),
            (1, ["D"]),
            (2, ["E", "F"]),
            (3, [])
        ]

        expected = [
            (0, "A"),
            (0, "B"),
            (0, "C"),
            (1, "D"),
            (2, "E"),
            (2, "F")
        ]

        self.assertListEqual(list(explode(a, itemgetter(1))), expected)

    def test_merge_dicts(self):
        """
        'merge_dicts([d1, d2])' should merge a list of dicts by merging each key
       """

        self.assertEqual(merge_dicts([]), {})

        self.assertEqual(merge_dicts([{'a': 1}, {}, {}]), {'a': 1})

        self.assertEqual(
            merge_dicts([{'a': {'x': 1}}, {'a': {'y': 2}, 'b': 2}]),
            {'a': {'x': 1, 'y': 2}, 'b': 2}
        )

        self.assertEqual(
            merge_dicts([{'a': {'x': 1}}, {'a': {'y': 2, 'x': 2}, 'b': 2}]),
            {'a': {'x': 2, 'y': 2}, 'b': 2}
        )

        self.assertEqual(
            merge_dicts([{'a': {'x': 1}}, {'a': {'y': 2, 'x': 2}, 'b': 2}, {'c': {'v': 10}}]),
            {'a': {'x': 2, 'y': 2}, 'b': 2, 'c': {'v': 10}}
        )
