import unittest

from test.utils.fakeResponse import fake_response_from_file
from opportunities.spiders.lowkey import LowkeySpider
from scrapy.http import Response, Request
from opportunities.items import OpportunitiesItem, AdItem

import pdb

class LowKeySpiderTest(unittest.TestCase):
    
    def setUp(self):
        self.spider = LowkeySpider()
    
    def test_main_results_page_parse_yields_url(self):
        main_results = self.spider.parse(fake_response_from_file("../templates/main_search.html"))
        result = list(main_results)[0]
        self.assertIsInstance(result, Request)

    def test_main_results_contain_ads_from_current_date(self):
        main_results = self.spider.parse(fake_response_from_file("../templates/main_search.html"))
        result = list(main_results)
        self.assertGreater(len(result), 1)

    def test_ad_results_page_parse(self):
        ad_results = self.spider.parse_ad(fake_response_from_file("../templates/ad.html"))
        result = list(ad_results)[0]
        self.assertIn('category', result)
        self.assertIn('date', result)
        self.assertIn('ad_post', result)
        self.assertIn('title', result)
        self.assertIn('ad_url', result)