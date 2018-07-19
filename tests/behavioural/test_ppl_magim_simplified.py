import re

from unittest import TestCase

from graphify.parser import Parser


class TestBuildGraph(TestCase):
    @classmethod
    def setUpClass(cls):

        #  text sample
        cls.text = [
            "Schedule 1 - GENERAL INVESTMENT GUIDELINES",
            "  28",
            "PPL – MAGIM FInal",
            "PART 1- INVESTMENT RESTRICTIONS",
            "The Manager must pay due regard to Applicable Laws and Regulations governing admissibility and permissibility of assets. The Manager may knowingly invest in assets which are impermissible only subject to the prior written approval of the Chief Actuary of the Client.",
            "Derivatives will be used only in a manner consistent with the usage restrictions described in the Applicable Laws and Regulations.",
            "1. General Restrictions",
            "1.1. The basic restrictions applicable to the Assets are specified in the PRA and/or FCA's Permitted Links Rules in its Conduct of Business Sourcebook (COBS). and the Prudential Sourcebook for Insurers (INSPRU).",
            "1.2. The Client has determined that such basic restrictions, specified in paragraph 1 above, should be supplemented by:",
            "1.2.1 the general terms contained within this Agreement; and",
            "1.2.2 detailed restrictions specified in this Schedule 1 or in the relevant portion of Schedule 2",
            "1.3. There shall be no negative currency exposures other than in relation to the Funds specified in paragraph 2.2.1 below but always subject to any constraints contained in Paragraph 1.1 of this Schedule.",
            "2. Derivative Restrictions",
            "2.1. Specific restrictions",
            "2.1.1 Permitted exchanges and contracts",
            "Instruments must be listed(1) or with an approved counterparty(1) and must be capable of being readily, closed out at a price the basis of which is pre-determined.",
            "Any exchange traded derivative that qualifies as a permitted link shall be allowed for efficient portfolio management purposes within any PPL Fund. In addition, the Manager may purchase and sell listed Warrants.",
            "2.1.2 Counterparty Restrictions",
            "Forward Currency Contracts are restricted to those transacted with banks identified on the “Approved Bank Counterparties” list maintained by the Manager’s Treasury. A copy of this list can be made available to the Client on request. Refer to Schedule 2 for fund specific restrictions. In the event of any conflict between the terms of Schedule 1 and Schedule 2, the terms of the latter shall prevail.",

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
            'components': ['Schedule', 'Part', 'Section', 'Point', 'Subpoint'],
            'patterns': [r'^Schedule\s\d{1,2}', r'^PART\s\d{1,2}', r'^\d{1,2}\.\s', r'^\d{1,2}\.\d{1,2}\.\s', r'^\d{1,2}\.\d{1,2}\.\d{1,2}\s']
        }

        p = Parser(descriptor)

        doc = p.parse(self.text)

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

