#!/usr/bin/env python

from unittest.mock import MagicMock, Mock, PropertyMock
import mock
import unittest

from testdata import *
from hyperlinks import *


# Mock out the requests.get call with the actual text from example.com and iana.org/domains/reserved
# Make sure the correct set is returned
class ScrapeLinksTestCase(unittest.TestCase):
    @mock.patch('hyperlinks.requests.get')
    def test_ScrapeHyperlinks(self, fake_get):
        # Create a fake response object to be returned by the patched requests.get call
        mockResponse = Mock()
        # Set the text property of the mock object so that we can access it in scrapeHyperlinksFromURL
        mockResponse.text = example_dot_com
        fake_get.return_value = mockResponse

        e = scrapeHyperlinksFromURL('http://www.example.com')
        self.assertEqual(e, {'https://www.iana.org/domains/example/'})

    @mock.patch('hyperlinks.requests.get')
    def test_ScrapeHyperlinks2(self, fake_get):
        # Create a fake response object to be returned by the patched requests.get call
        mockResponse = Mock()
        # Set the text property of the mock object so that we can access it in scrapeHyperlinksFromURL
        mockResponse.text = iana_reserved_domains
        fake_get.return_value = mockResponse

        e = scrapeHyperlinksFromURL('https://www.iana.org/domains/reserved')

        self.assertCountEqual(e, iana_linkset)
