import re

from unittest import TestCase

from graphify.build.traverse import build
from graphify.descriptor.utils import compile_patterns


class TestBuildGraph(TestCase):
    @classmethod
    def setUpClass(cls):

        #  text sample
        cls.text = [
            "NOW IT IS HEREBY AGREED as follows:",
            "1. INTERPRETATION",
            "1.1 In this Agreement and in the Recitals, the following expressions shall have the following meanings.",
            "(a) the determination and communication of the investment",
            "(b) the issuance of written instructions to the Manager",
            "(c) the provisions of any Instructions by the Client from time to time;.",
            "2. MANAGEMENT",
            "2A. The Manager shall manage such assets (including cash)",
            "2A.1 The Manager shall ensure that it has in place all the policies and procedures",
            "2.13A The Manager shall manage the Assets in accordance with the Guidelines.",
            "Subject to the Guidelines, the Manager shall have complete discretion.",
            "",
            "3B CUSTODY AND REGISTRATION",
            "3B.1 The Manager shall (as agent of the Client), with the prior approval of the Client.",
            "Appoint one or more custodians of securities (each a 'Custodian')",
            "",
            "4. DEALINGS AND SETTLEMENT",
            "4.1 The Manager shall effect dealings for the Assets through clearers.",
            "4.2 Without prejudice to Clause 3.3, the Manager shall ensure that prompt notice of all dealings",
            "4.3. Subject to PRA and/or FCA Rules, the Manager may aggregate transactions",
            "4.4 Specific instructions from the Client in relation to the execution of orders.",
        ]


    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_graph_is_correctly_build(self):
        """
        Given an iterable content plus a hierarchy descriptor, we should be able to build a graph with
        that captures the content structure
        """
        descriptor = {
            'components': ['Section', 'Subsection'],
            'patterns': [r'^\d{1,2}[A-Z]?\.?\s', r'^\d{1,2}[A-Z]?\.\d{1,2}\s']
        }

        descriptor = compile_patterns(descriptor)

        graph = build(self.text, descriptor)

        def identifier(x):
            reg = re.compile(r'\[(\d+\_?(\d+)?)[a-z]?\]')
            return int(reg.search(x).groups(0)[0])

        reading_order = sorted(graph.nodes(), key=identifier)

        self.assertListEqual(reading_order, [
            "ROOT [0]",
            "1. [1]",
            "1.1 [2]",
            "2. [3]",
            "2A. [4]",
            "2A.1 [5]",
            "3B [6]",
            "3B.1 [7]",
            "4. [8]",
            "4.1 [9]",
            "4.2 [10]",
            "4.4 [11]",
        ])

        self.assertDictEqual(
            graph.node["2. [3]"],
            {'content': ['2. MANAGEMENT'], 'level': 1, 'meta': '2.', 'pad': 0},
        )

        self.assertDictEqual(
            graph.node["3B [6]"],
            {'meta': '3B', 'level': 1, 'pad': 0, 'content': ['3B CUSTODY AND REGISTRATION']}
        )

        self.assertDictEqual(
            graph.node["4.2 [10]"],
            {
                'level': 2,
                'pad': 0,
                'content': [
                    '4.2 Without prejudice to Clause 3.3, the Manager shall ensure that prompt notice of all dealings',
                    '4.3. Subject to PRA and/or FCA Rules, the Manager may aggregate transactions'
                ],
                'meta': '4.2'
            }
        )

    def test_stop_marker(self):
        """
        We should be able to provide a stopping pattern at the descriptor
        """
        descriptor = {
            'components': ['Section', 'Subsection'],
            'patterns': [r'^\d{1,2}[A-Z]?\.?\s', r'^\d{1,2}[A-Z]?\.\d{1,2}\s'],
            'stopParsing': r'^Appoint'
        }

        descriptor = compile_patterns(descriptor)

        graph = build(self.text, descriptor)

        def identifier(x):
            reg = re.compile(r'\[(\d+\_?(\d+)?)[a-z]?\]')
            return int(reg.search(x).groups(0)[0])

        reading_order = sorted(graph.nodes(), key=identifier)

        self.assertListEqual(reading_order, [
            "ROOT [0]",
            "1. [1]",
            "1.1 [2]",
            "2. [3]",
            "2A. [4]",
            "2A.1 [5]",
            "3B [6]",
            "3B.1 [7]"
        ])

        self.assertDictEqual(
            graph.node["2. [3]"],
            {'content': ['2. MANAGEMENT'], 'level': 1, 'meta': '2.', 'pad': 0},
        )

        self.assertDictEqual(
            graph.node["3B [6]"],
            {'meta': '3B', 'level': 1, 'pad': 0, 'content': ['3B CUSTODY AND REGISTRATION']}
        )

    def test_start_parsing(self):
        """
        We should be able to provide a starting pattern to point out the start of the relevant content
        """
        descriptor = {
            'components': ['Section', 'Subsection'],
            'patterns': [r'^\d{1,2}[A-Z]?\.?\s', r'^\d{1,2}[A-Z]?\.\d{1,2}\s'],
            'startParsing': r'the provisions of any'
        }

        descriptor = compile_patterns(descriptor)

        graph = build(self.text, descriptor)

        def identifier(x):
            reg = re.compile(r'\[(\d+\_?(\d+)?)[a-z]?\]')
            return int(reg.search(x).groups(0)[0])

        reading_order = sorted(graph.nodes(), key=identifier)

        self.assertListEqual(reading_order, [
            "ROOT [0]",
            "2. [1]",
            "2A. [2]",
            "2A.1 [3]",
            "3B [4]",
            "3B.1 [5]",
            "4. [6]",
            "4.1 [7]",
            "4.2 [8]",
            "4.4 [9]",
        ])

        self.assertDictEqual(
            graph.node["2. [1]"],
            {'content': ['2. MANAGEMENT'], 'level': 1, 'meta': '2.', 'pad': 0},
        )

        self.assertDictEqual(
            graph.node["3B [4]"],
            {'meta': '3B', 'level': 1, 'pad': 0, 'content': ['3B CUSTODY AND REGISTRATION']}
        )

        self.assertDictEqual(
            graph.node["4.2 [8]"],
            {
                'level': 2,
                'pad': 0,
                'content': [
                    '4.2 Without prejudice to Clause 3.3, the Manager shall ensure that prompt notice of all dealings',
                    '4.3. Subject to PRA and/or FCA Rules, the Manager may aggregate transactions'
                ],
                'meta': '4.2'
            }
        )
