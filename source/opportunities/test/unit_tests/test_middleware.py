import unittest

from opportunities.middlewares import IgnoreDuplicateAdsRequestMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.http import Request
from unittest.mock import Mock, patch
from scrapy.spider import Spider

class MiddlewareTest(unittest.TestCase):

    def _store_on_first_return_on_subsequent(self):
        """Side effect function for mock of redis cache to simulate set and get"""
        yield None
        while True:
            yield 1
    
    def _prepare_mocked_cache_conn(self):
        """Mocks redis cache connection along with its get method"""
        mock_cache_conn = Mock()
        mock_cache_conn.get()
        mock_cache_conn.get.side_effect = self._store_on_first_return_on_subsequent()
        return mock_cache_conn

    @patch('opportunities.middlewares.IgnoreDuplicateAdsRequestMiddleware.__init__')
    def _prepare_mocked_dup_middleware(self, mock__init__):
        """Mocks init function to use connections to redis cache or database"""
        mock__init__.return_value = None
        middleware = IgnoreDuplicateAdsRequestMiddleware()
        middleware.cache_conn = self._prepare_mocked_cache_conn()
        return middleware
    
    def test_dup_middleware_throws_exception_on_dups(self):
        middleware = self._prepare_mocked_dup_middleware()
        request = Request(url='https://madison.craigslist.org/fbh/d/food-cart-restaurant-seeking/6608401431.html')
        spider = Spider(name="Jim")
        middleware.process_request(request, spider)
        with self.assertRaises(IgnoreRequest):
            middleware.process_request(request, spider)
        