import unittest

from utils import fakeResponse
import spiders.lowkey
from scrapy.http import Response, Request

class UtilsTest(unittest.TestCase):
    res = fakeResponse("./templates/main_search.html")
    self.assertIsInstance(res, Response)

# class LowKeySpiderTest(unittest.TestCase):
    
#     def setUp(self):
#         self.spider = lowkey.LowkeySpider()
    
#     def 

if name == "__main__":
    unittest.main(warnings=ignore)