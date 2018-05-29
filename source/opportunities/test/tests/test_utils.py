import unittest

from opportunities.test.utils.fakeResponse import fake_response_from_file
from opportunities.opportunities.spiders.lowkey import LowkeySpider
from scrapy.http import Response, Request

class UtilsTest(unittest.TestCase):

    def test_stuff(self):
        res = fake_response_from_file("../templates/main_search.html")
        self.assertIsInstance(res, Response)

# class LowKeySpiderTest(unittest.TestCase):
    
#     def setUp(self):
#         self.spider = lowkey.LowkeySpider()
    
#     def 
