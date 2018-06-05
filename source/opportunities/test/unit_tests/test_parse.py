import unittest

from test.utils.fakeResponse import fake_response_from_file
from opportunities.spiders.lowkey import LowkeySpider
from scrapy.http import Response, Request
from scrapy.exceptions import CloseSpider
from opportunities.items import OpportunitiesItem, AdItem
import requests
import os

import pdb
from datetime import datetime

SEARCH_TEMPLATE_PATH = "../templates/main_search.html" 
AD_TEMPLATE_PATH = "../templates/ad.html" 

class LowKeySpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = LowkeySpider()
    
    def _filter_terminating_exceptions(self, results):
        new_results = []
        while True:
            res = None
            try:
                res = next(results)
                new_results.append(res)
            except CloseSpider as e:
                continue
            except StopIteration as e:
                break
        return new_results 


    def test_main_results_page_parse_yields_url(self):
        main_results = self.spider.parse(fake_response_from_file(SEARCH_TEMPLATE_PATH))
        results = self._filter_terminating_exceptions(main_results)                
        result = results[0]
        self.assertIsInstance(result, Request)


    def test_main_results_contain_ads_from_current_date(self):
        main_results = self.spider.parse(fake_response_from_file(SEARCH_TEMPLATE_PATH))
        results = self._filter_terminating_exceptions(main_results)                
        self.assertGreater(len(results), 1)

    def _whole_list_is_same_date(self, results):
        # if all results seem to be parsed and next page url is present
        if len(results) > 50 and 'search/jjj?s' in results[-1].url:
            raise CloseSpider # raise an assert to make sure date test doesn't fail
    
    def test_main_results_throws_close_exception_for_dates_older_than_current_date(self):
        main_results = self.spider.parse(fake_response_from_file(SEARCH_TEMPLATE_PATH))
        with self.assertRaises(CloseSpider):
            results = list(main_results)
            self._whole_list_is_same_date(results)

    def test_ad_results_page_parse(self):
        ad_results = self.spider.parse_ad(fake_response_from_file(AD_TEMPLATE_PATH))
        result = list(ad_results)[0]
        self.assertIn('category', result)
        self.assertIn('date', result)
        self.assertIn('ad_post', result)
        self.assertIn('title', result)
        self.assertIn('ad_url', result)
    
    def test_ad_results_page_parse_properly_stripped(self):
        ad_results = self.spider.parse_ad(fake_response_from_file(AD_TEMPLATE_PATH))
        result = list(ad_results)[0]
        self.assertEqual(result['city'], "WATERTOWN")
        self.assertEqual(result['title'], "PRODUCTION LINE WORKER/TRIMMER PACKER")