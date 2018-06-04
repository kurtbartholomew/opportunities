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

    @staticmethod
    def _resolve_path(path):
        return os.path.abspath(os.path.join(os.path.dirname(__file__),path))

    @classmethod
    def setUpClass(cls):
        path = cls._resolve_path(SEARCH_TEMPLATE_PATH)
        up_to_date = False
        if os.path.isfile(path):
            stats = os.stat(path)
            if datetime.now().day == datetime.fromtimestamp(stats.st_mtime).day:
                up_to_date = True
        
        if not up_to_date:
            res = requests.get(LowkeySpider.start_urls[0])
            pdb.set_trace()
            with open(path, 'w') as search:
                search.write(res.text)
    
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
        pdb.set_trace()
        self.assertGreater(len(results), 1)
    
    # This test may fail if the whole current front page has job postings
    # from the current date. This does not really happen but is something to watch for.
    # Requests are returned, so checking for dates is not really an option
    def test_main_results_throws_close_exception_for_dates_older_than_current_date(self):
        main_results = self.spider.parse(fake_response_from_file(SEARCH_TEMPLATE_PATH))
        with self.assertRaises(CloseSpider):
            results = list(main_results)

    def test_ad_results_page_parse(self):
        ad_results = self.spider.parse_ad(fake_response_from_file(AD_TEMPLATE_PATH))
        result = list(ad_results)[0]
        self.assertIn('category', result)
        self.assertIn('date', result)
        self.assertIn('ad_post', result)
        self.assertIn('title', result)
        self.assertIn('ad_url', result)