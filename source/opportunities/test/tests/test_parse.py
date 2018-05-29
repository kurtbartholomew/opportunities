import unittest

from opportunities.test.utils.fakeResponse import fake_response_from_file
from opportunities.opportunities.spiders.lowkey import LowkeySpider
from scrapy.http import Response, Request

class LowKeySpiderTest(unittest.TestCase):
    
    def setUp(self):
        self.spider = LowkeySpider()
    
    def test_parse(self):

        results = self.spider.parse(fake_response_from_file("../templates/main_search.html"))
