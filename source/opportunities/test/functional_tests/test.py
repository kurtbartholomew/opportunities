import unittest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from opportunities.spiders.lowkey import LowkeySpider
from opportunities.persistence.models import Ad
from opportunities.persistence.db import Database
from sqlalchemy.orm import sessionmaker

import pdb

TEST_DB_LOCATION = 'file:source/opportunities/test/test.db'

TEST_SETTINGS = {
    'DOWNLOAD_DELAY': 15,
    'CLOSESPIDER_PAGECOUNT': 3,
    'CLOSESPIDER_ITEMCOUNT' : 3,
    'USER_AGENT' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0',
    'COOKIES_ENABLED': False,
    'CONCURRENT_REQUESTS' : 1,
    'LOG_LEVEL': 'DEBUG',
    'LOG_STDOUT': True,
    'LOG_FILE': 'logs/test_opportunities.log'
}

TEST_PIPELINES = {
    'test.utils.testPipeline.TestOpportunitiesPipeline' : 0
}

class FunctionalTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        db = Database(config={'database':'test_opportunities'})
        self.engine = db.get_engine()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def setUp(self):
        self.process = CrawlerProcess(get_project_settings()) 
        # settings are updated to scrape a very small amount of pages very slowly
        self.process.settings.update(TEST_SETTINGS)
        # settings are updated to funnel items into a test database pipeline
        self.process.settings.get('ITEM_PIPELINES').update(TEST_PIPELINES)
        

    def test_scraping_live_page_returns_valid_results(self):
        self.process.crawl(LowkeySpider)
        self.process.start()
        row = self.session.query(Ad).first()
        self.assertNotEqual(row, None)

    @classmethod
    def tearDownClass(self):
        self.session.close_all()
        self.session.close()
        self.engine.dispose()

if __name__ == "__main__":
    unittest.main()