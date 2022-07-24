#!/usr/bin/env python

import mock
import unittest

from testdata import *
from hyperlinks import *

# 200 IQ way of mocking a requests.get() call with a 'text' attribute
class DummyResponse:
    def __init__(self, text):
        self.text = text

# Mock out the requests.get call with the actual text from example.com and iana.org/domains/reserved
# Make sure the correct link array is returned
class ScrapeLinksTestCase(unittest.TestCase):
    @mock.patch('hyperlinks.requests.get')
    def test_ScrapeHyperlinks(self, fake_get):
        # Create a fake response object
        response = DummyResponse(example_dot_com)
        fake_get.return_value = response

        e = scrapeHyperlinksFromURL('http://www.example.com')
        self.assertEqual(e, ['https://www.iana.org/domains/example'])

    @mock.patch('hyperlinks.requests.get')
    def test_ScrapeHyperlinks2(self, fake_get):
        # Create a fake response object
        response = DummyResponse(iana_reserved_domains)
        fake_get.return_value = response

        e = scrapeHyperlinksFromURL('https://www.iana.org/domains/reserved')
        self.assertEqual(e, iana_linklist)
