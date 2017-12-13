import re

from unittest import TestCase

from graphify.descriptor.utils import compile_patterns


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
            self.assertEqual(str(pattern.__class__), "<class '_sre.SRE_Pattern'>")

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








