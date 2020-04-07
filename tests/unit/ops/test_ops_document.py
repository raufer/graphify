import re

from unittest import TestCase

from functools import reduce

from graphify.backbone.networkx import NetworkxImplementation
from graphify.build.graph import _add_node
from graphify.build.initialization import initialize_backbone
from graphify.ops.document import copy, map_values
from graphify.parsing import parse_iterable

# During the parsing process some information is added to the document representation to
# allow to parsing to proceed
# Given a 'descriptor' we take every 'exclude' pattern and remove every occurrence from the
# document body


class TestOpsDocument(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_copy(self):
        it = [
            "[[C]] Chapter I",
            "This is chapter I text",
            "[[A]] Article I",
            "This is article I text",
            "[[A]] Article II",
            "This is article II text"
        ]

        descriptor = {
            'components': ['Chapter', 'Article'],
            'patterns': ['C', 'A']
        }

        doc = parse_iterable(it, descriptor)

        for key, n in doc.traverse():
            n['level'] = 0

        new_doc = copy(doc)

        for key, n in new_doc.traverse():
            n['level'] = 1

        n = len(list(doc.traverse()))

        self.assertListEqual(
            [n['level'] for i, n in doc.traverse()],
            [0] * n
        )

        self.assertListEqual(
            [n['level'] for i, n in new_doc.traverse()],
            [1] * n
        )

    def test_map_data(self):
        """
        Map a particular field of every document node with a arbitrary function f
        `map_values` should be an immutable operation
        """
        it = [
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
            "[[Article]] Article II",
            "This is article II text"
        ]

        descriptor = {
            'components': ['Chapter', 'Article'],
            'patterns': ['Chapter', 'Article']
        }

        doc = parse_iterable(it, descriptor)
        doc_level = [n['level'] for _, n in doc.traverse()]

        def f(data):
            data['level'] = 100

        new_doc = map_values(doc, f)

        result = [n['level'] for _, n in new_doc.traverse()]
        expected = [100] * len(result)

        self.assertListEqual(result, expected)

        self.assertListEqual(doc_level, [n['level'] for _, n in doc.traverse()])

    def test_map_data_example_map_text(self):
        """
        Return a new document with the text field processed
        """
        it = [
            "Schedule 1 - First Part",
            " -- 100",
            "PPL – Final",
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
            "[[Article]] Article II",
            "This is article II text"
        ]

        descriptor = {
            'components': ['Schedule', 'Chapter', 'Article'],
            'patterns': [r'^Schedule\s\d{1,2}', 'Chapter', 'Article']
        }

        doc = parse_iterable(it, descriptor)

        descriptor['exclude'] = [
            re.compile('\\[\\[^Schedule\\s\\d{1,2}\\]\\]'),
            re.compile('\\[\\[Chapter\\]\\]\s',),
            re.compile('\\[\\[Article\\]\\]\s')
        ]

        def remove_occurrences(data):
            data['content'] = [
                reduce(lambda acc, x: x.sub('', acc), descriptor['exclude'], line)
                for line in data['text']
            ]
            return data

        new_doc = map_values(doc, remove_occurrences)

        result = [n['content'] for _, n in new_doc.traverse()]

        expected = [
            [],
            [
                "Schedule 1 - First Part",
                " -- 100",
                "PPL – Final",
            ],
            [
                "Chapter I",
                "This is chapter I text",
            ],
            [
                "Article I",
                "This is article I text",
            ],
            [
                "Article II",
                "This is article II text"
            ]

        ]

        self.assertListEqual(result, expected)

