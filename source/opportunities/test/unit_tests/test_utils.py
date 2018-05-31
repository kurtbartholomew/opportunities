import unittest

from test.utils.fakeResponse import fake_response_from_file
from opportunities.spiders.lowkey import LowkeySpider
from scrapy.http import Response, Request
from scrapy.selector import Selector

import pdb
class UtilsTest(unittest.TestCase):

    def test_fake_response_from_file(self):
        res = fake_response_from_file("../templates/main_search.html")
        self.assertIsInstance(res, Response)
        self.assertIn('jobs  - craigslist', res.text)
