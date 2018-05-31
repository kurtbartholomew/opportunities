import unittest
import sys, os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
sys.path.append(os.path.abspath('.'))

from opportunities.spiders.lowkey import LowkeySpider

import pdb

class FunctionalTest(unittest.TestCase):

    def test_crawling_on_live_page(self):
        spider = LowkeySpider()

        process = CrawlerProcess(get_project_settings())

        # 'followall' is the name of one of the spiders of the project.
        process.crawl('lowkey')
        process.start() # the script will block here until the crawling is finished


if __name__ == "__main__":
    unittest.main()