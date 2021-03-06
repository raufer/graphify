import re

from unittest import TestCase

from graphify.descriptor.search import search_descriptor_patterns
from graphify.descriptor.utils import compile_patterns, normalize_descriptor


class TestDescriptorUtils(TestCase):
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

    def test_search_descriptor_patterns(self):
        """
        Given a descriptor configuration object every 'pattern' should be compile
        """
        descriptor = {
            'components': ['A', 'B', 'C'],
            'patterns': [r'A', r'B', r'C']
        }

        descriptor = compile_patterns(descriptor)
        descriptor = normalize_descriptor(descriptor)

        self.assertEqual(search_descriptor_patterns('A', descriptor)[1], 1)
        self.assertEqual(search_descriptor_patterns('B', descriptor)[1], 2)
        self.assertEqual(search_descriptor_patterns('C', descriptor)[1], 3)
        self.assertEqual(search_descriptor_patterns('X', descriptor)[1], None)

    def test_search_descriptor_patterns_different_components_same_hierarchy(self):
        descriptor = {
            'components': [['A', 'Z'], 'B', 'C'],
            'patterns': [[r'A', r'Z'], r'B', r'C']
        }

        descriptor = compile_patterns(descriptor)
        descriptor = normalize_descriptor(descriptor)

        self.assertEqual(search_descriptor_patterns('A', descriptor)[1], 1)
        self.assertEqual(search_descriptor_patterns('Z', descriptor)[1], 1)
        self.assertEqual(search_descriptor_patterns('B', descriptor)[1], 2)
        self.assertEqual(search_descriptor_patterns('C', descriptor)[1], 3)
        self.assertEqual(search_descriptor_patterns('X', descriptor)[1], None)
