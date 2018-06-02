import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from opportunities.spiders.lowkey import LowkeySpider

import pdb
import sqlite3

TEST_DB_LOCATION = 'file:source/opportunities/test/test.db'

TEST_SETTINGS = {
    'DOWNLOAD_DELAY': 15,
    'CLOSESPIDER_PAGECOUNT': 3,
    'CLOSESPIDER_ITEMCOUNT' : 3,
    'USER_AGENT' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0',
    'COOKIES_ENABLED': False,
    'CONCURRENT_REQUESTS' : 1,
    'LOG_LEVEL': 'ERROR'
}

TEST_PIPELINES = {
    'test.utils.testPipeline.TestOpportunitiesPipeline' : 0
}

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.process = CrawlerProcess(get_project_settings()) 
        # settings are updated to scrape a very small amount of pages very slowly
        self.process.settings.update(TEST_SETTINGS)
        # settings are updated to funnel items into a test database pipeline
        self.process.settings.get('ITEM_PIPELINES').update(TEST_PIPELINES)
        

    def test_scraping_live_page_returns_valid_results(self):
        self.process.crawl(LowkeySpider)
        self.process.start()
        conn = sqlite3.connect(TEST_DB_LOCATION)
        c = conn.cursor()
        results = c.execute('SELECT title FROM ads limit 5')
        rows = results.fetchall()
        self.assertNotEqual(len(rows), 0)
        conn.close()
        


if __name__ == "__main__":
    unittest.main()