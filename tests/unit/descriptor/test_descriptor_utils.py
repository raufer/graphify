import re

from unittest import TestCase

from graphify.descriptor.utils import compile_patterns, extend_internal_patterns

from hypothesis import given
from hypothesis import strategies as st


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

    def test_pattern_compiling(self):
        """
        Given a descriptor configuration object every 'pattern' should be compile
        """
        descriptor = {
            'components': ['A', 'B', 'C'],
            'patterns': [r'A', r'B', r'C']
        }

        compiled_descriptor = compile_patterns(descriptor)

        self.assertListEqual(compiled_descriptor['components'], ['A', 'B', 'C'])

        for pattern in compiled_descriptor['patterns']:
            self.assertEqual(str(pattern.__class__), "<class 're.Pattern'>")

    def test_extend_internal_patterns_example(self):
        """
        Utility method. Given a descriptor configuration extend the patterns to support internal patterns
        e.g. 'patterns': [r'A', r'B', r'C'] -> [r'A', r'B', r'C']
        """
        descriptor = {
            'components': ['A', 'B', 'C'],
            'patterns': [r'A', r'B', r'C']
        }

        expected = {
            'components': ['A', 'B', 'C'],
            'patterns': [r'(?:\[\[(A)\]\]|(A))', r'(?:\[\[(B)\]\]|(B))', r'(?:\[\[(C)\]\]|(C))'],
            'exclude': [r'\[\[A\]\]\s?', r'\[\[B\]\]\s?', r'\[\[C\]\]\s?']
        }

        result = extend_internal_patterns(descriptor)
        self.assertDictEqual(result, expected)

    def test_pattern_compiling_with_flags(self):
        """
        Given a descriptor configuration object the patterns can be regex objects if the user need a higher flexibility
        """
        descriptor = {
            'components': ['A', 'B', 'C'],
            'patterns': [re.compile(r'A'), re.compile(r'B'), re.compile(r'C')]
        }

        compiled_descriptor = compile_patterns(descriptor)

        self.assertDictEqual(descriptor, compiled_descriptor)








