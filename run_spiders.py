import sys, os

sys.path.insert(0, os.path.join(os.path.abspath('.'), 'source/opportunities'))
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'source/opportunities/opportunities'))

import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.project import get_project_settings
from opportunities.spiders.lowkey import LowkeySpider

import logging
from main_logging import configure_scrapy_log
configure_scrapy_log('logs/opportunities.log', log_level=logging.ERROR)
os.environ['SCRAPY_SETTINGS_MODULE'] = 'opportunities.settings'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run scrapers')
    args = parser.parse_args()

    process = CrawlerProcess(get_project_settings()) 
    process.crawl(LowkeySpider)
    process.start()
    