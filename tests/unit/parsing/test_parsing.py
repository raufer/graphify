import re

from unittest import TestCase

from graphify.descriptor.utils import extend_internal_patterns, compile_patterns
from graphify.parsing import parse_iterable, post_build_process


class TestBuildGraph(TestCase):
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

    def test_parse_iterable(self):
        """
        Given an iterable content plus a hierarchy descriptor, we should be able to build a graph with
        that captures the content structure
        """
        it = [
            "Schedule 1 - First Part",
            " -- 100",
            "PPL – FInal",
            "PART 1- INVESTMENT RESTRICTIONS",
            "The Manager must pay due regard to Applicable Laws and Regulations",
            "Derivatives will be used only in a manner consistent with the usage restrictions",
            "1. General Restrictions",
            "1.1. The basic restrictions applicable to the Assets specified in the PRA",
            "1.2. The Client has determined that such basic restrictions should be supplemented by:",
            "1.2.1 the general terms contained within this Agreement; and",
            "1.2.2 the terms agreed in previous regulations",
            "1.3. There shall be no negative currency exposures specified in paragraph 2.2.1",
            "2. Derivative Restrictions",
            "2.1. Specific restrictions",
            "2.1.1 Permitted exchanges and contracts",
            "Instruments must be listed(1) or with an approved counterparty(1)",
            "2.1.2 Counterparty Restrictions",
            "Forward Currency Contracts are restricted to those transacted with banks",
        ]

        descriptor = {
            'components': ['Schedule', 'Part', 'Section', 'Point', 'Subpoint'],
            'patterns': [r'^Schedule\s\d{1,2}', r'^PART\s\d{1,2}', r'^\d{1,2}\.\s', r'^\d{1,2}\.\d{1,2}\.\s', r'^\d{1,2}\.\d{1,2}\.\d{1,2}\s']
        }

        doc = parse_iterable(it, descriptor)

        def identifier(x):
            reg = re.compile(r'\[(\d+\_?(\d+)?)[a-z]?\]')
            return int(reg.search(x).groups(0)[0])

        reading_order = sorted(doc.graph.nodes(), key=identifier)

        self.assertListEqual(reading_order, [
            "ROOT [0]",
            "Schedule 1 [1]",
            "PART 1 [2]",
            "1. [3]",
            "1.1. [4]",
            "1.2. [5]",
            "1.2.1 [6]",
            "1.2.2 [7]",
            "1.3. [8]",
            "2. [9]",
            "2.1. [10]",
            "2.1.1 [11]",
            "2.1.2 [12]"
        ])

    def test_post_build_processing_remove_occurrences(self):
        """
        Given an iterable content plus a hierarchy descriptor, we should be able to build a graph with
        that captures the content structure
        """
        it = [
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
        ]

        descriptor = {
            'components': ['Chapter', 'Article'],
            'patterns': ['Chapter', 'Article']
        }

        doc = parse_iterable(it, descriptor)

        descriptor = extend_internal_patterns(descriptor)
        descriptor = compile_patterns(descriptor)

        doc = post_build_process(doc, descriptor)

        result = [n['text'] for _, n in doc.traverse()]
        expected = [[], ["Chapter I", "This is chapter I text"], ["Article I", "This is article I text"]]
        self.assertListEqual(result, expected)

    def test_hierarchy_jumps(self):
        """
        Jumps in hierarchy should be allowed
        """
        it = [
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
        ]

        descriptor = {
            'components': ['Chapter', 'Section', 'Sub-section', 'Article'],
            'patterns': ['Chapter', 'Section', 'Sub-section', 'Article']
        }

        doc = parse_iterable(it, descriptor)

        def identifier(x):
            reg = re.compile(r'\[(\d+\_?(\d+)?)[a-z]?\]')
            return int(reg.search(x).groups(0)[0])

        reading_order = sorted(doc.graph.nodes(), key=identifier)

        expected = [
            "ROOT [0]",
            "Chapter [1]",
            "Article [2]",
        ]

        self.assertListEqual(reading_order, expected)

    def test_simple_parsing(self):
        it = [
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
        ]

        descriptor = {
            'components': ['Chapter', 'Section', 'Sub-section', 'Article'],
            'patterns': ['Chapter', 'Section', 'Sub-section', 'Article']
        }

        doc = parse_iterable(it, descriptor)

        result = [n for n in doc.graph.nodes(data=True)]

        expected = [
            ('ROOT [0]', {'meta': 'root', 'level': 0, 'text': [], 'pad': False, 'id': '/root'}),
            ('Chapter [1]', {'meta': 'Chapter', 'level': 1, 'pad': False, 'text': ["Chapter I", 'This is chapter I text'], 'id': '/root/chapter-1'}),
            ('Article [2]', {'meta': 'Article', 'level': 4, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/root/chapter-1/article-2'})
        ]

        self.assertListEqual(result, expected)

    def test_custom_ids(self):
        """
        Some sources are already structured and contain node IDs
        that map back to valid URIs

        In these cases we should be able to use these instead of
        creating new ones internally
        """
        it = [
            "[[Chapter]]{'id': '/base/chapter/1'} Chapter I",
            "This is chapter I text",
            "[[Article]]{'id': '/base/article/1'} Article I",
            "This is article I text",
        ]

        descriptor = {
            'components': ['Chapter', 'Section', 'Sub-section', 'Article'],
            'patterns': ['Chapter', 'Section', 'Sub-section', 'Article']
        }

        doc = parse_iterable(it, descriptor)

        result = [n for n in doc.graph.nodes(data=True)]

        expected = [
            ('ROOT [0]', {'meta': 'root', 'level': 0, 'text': [], 'pad': False, 'id': '/root'}),
            ('Chapter [1]', {'meta': 'Chapter', 'level': 1, 'pad': False, 'text': ["Chapter I", 'This is chapter I text'], 'id': '/base/chapter/1'}),
            ('Article [2]', {'meta': 'Article', 'level': 4, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/base/article/1'})
        ]

        self.assertListEqual(result, expected)

    def test_different_components_with_the_same_hierarchy(self):
        it = [
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
            "[[Article]] Article II",
            "This is article II text",
            "[[Chapter]] Chapter II",
            "This is chapter II text",
            "[[Article]] Article I",
            "This is article I text",
            "[[Schedule]] Schedule I",
            "This is schedule I text",
            "[[Article]] Article I",
            "This is article I text",
        ]

        descriptor = {
            'components': [['Chapter', 'Schedule'], 'Section', 'Sub-section', 'Article'],
            'patterns': [['Chapter', 'Schedule'], 'Section', 'Sub-section', 'Article']
        }

        doc = parse_iterable(it, descriptor)

        result = [n for n in doc.graph.nodes(data=True)]

        expected = [
            ('ROOT [0]', {'meta': 'root', 'level': 0, 'text': [], 'pad': False, 'id': '/root'}),
            ('Chapter [1]', {'meta': 'Chapter', 'level': 1, 'pad': False, 'text': ["Chapter I", 'This is chapter I text'], 'id': '/root/chapter-1'}),
            ('Article [2]', {'meta': 'Article', 'level': 4, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/root/chapter-1/article-2'}),
            ('Article [3]', {'meta': 'Article', 'level': 4, 'pad': False, 'text': ["Article II", 'This is article II text'], 'id': '/root/chapter-1/article-3'}),
            ('Chapter [4]', {'meta': 'Chapter', 'level': 1, 'pad': False, 'text': ["Chapter II", 'This is chapter II text'], 'id': '/root/chapter-4'}),
            ('Article [5]', {'meta': 'Article', 'level': 4, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/root/chapter-4/article-5'}),
            ('Schedule [6]', {'meta': 'Schedule', 'level': 1, 'pad': False, 'text': ["Schedule I", 'This is schedule I text'], 'id': '/root/schedule-6'}),
            ('Article [7]', {'meta': 'Article', 'level': 4, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/root/schedule-6/article-7'})
        ]

        self.assertListEqual(result, expected)

    def test_document_with_gaps(self):
        it = [
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
            "[[Article]] Article II",
            "This is article II text",
            "[[Chapter]] Chapter II",
            "This is chapter II text",
            "[[Article]] Article I",
            "This is article I text",
            "[[Schedule]] Schedule I",
            "This is schedule I text",
            "[[Chapter]] Chapter I",
            "This is chapter I text",
            "[[Article]] Article I",
            "This is article I text",
        ]

        descriptor = {
            'components': ['Schedule', 'Chapter', 'Section', 'Sub-section', 'Article'],
            'patterns': ['Schedule', 'Chapter', 'Section', 'Sub-section', 'Article']
        }

        doc = parse_iterable(it, descriptor)

        result = [n for n in doc.graph.nodes(data=True)]

        expected = [
            ('ROOT [0]', {'meta': 'root', 'level': 0, 'text': [], 'pad': False, 'id': '/root'}),
            ('Chapter [1]', {'meta': 'Chapter', 'level': 2, 'pad': False, 'text': ["Chapter I", 'This is chapter I text'], 'id': '/root/chapter-1'}),
            ('Article [2]', {'meta': 'Article', 'level': 5, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/root/chapter-1/article-2'}),
            ('Article [3]', {'meta': 'Article', 'level': 5, 'pad': False, 'text': ["Article II", 'This is article II text'], 'id': '/root/chapter-1/article-3'}),
            ('Chapter [4]', {'meta': 'Chapter', 'level': 2, 'pad': False, 'text': ["Chapter II", 'This is chapter II text'], 'id': '/root/chapter-4'}),
            ('Article [5]', {'meta': 'Article', 'level': 5, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/root/chapter-4/article-5'}),
            ('Schedule [6]', {'meta': 'Schedule', 'level': 1, 'pad': False, 'text': ["Schedule I", 'This is schedule I text'], 'id': '/root/schedule-6'}),
            ('Chapter [7]', {'meta': 'Chapter', 'level': 2, 'pad': False, 'text': ["Chapter I", 'This is chapter I text'], 'id': '/root/schedule-6/chapter-7'}),
            ('Article [8]', {'meta': 'Article', 'level': 5, 'pad': False, 'text': ["Article I", 'This is article I text'], 'id': '/root/schedule-6/chapter-7/article-8'})
        ]

        self.assertListEqual(result, expected)



