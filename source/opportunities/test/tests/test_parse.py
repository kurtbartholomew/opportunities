import unittest

from opportunities.test.utils.fakeResponse import fake_response_from_file
from opportunities.opportunities.spiders.lowkey import LowkeySpider
from scrapy.http import Response, Request
from opportunities.opportunities.items import OpportunitiesItem, AdItem

import pdb

class LowKeySpiderTest(unittest.TestCase):
    
    def setUp(self):
        self.spider = LowkeySpider()
    
    def test_main_results_page_parse(self):
        main_results = self.spider.parse(fake_response_from_file("../templates/main_search.html"))
        result = list(main_results)[0]
        self.assertIsInstance(result, Request)

    def test_ad_results_page_parse(self):
        ad_results = self.spider.parse_ad(fake_response_from_file("../templates/ad.html"))
        result = list(ad_results)[0]
        self.assertIn('category', result)
        self.assertIn('date', result)
        self.assertIn('ad_post', result)
        self.assertIn('title', result)
        self.assertIn('ad_url', result)