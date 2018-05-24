# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OpportunitiesItem, AdItem

class LowkeySpider(CrawlSpider):
    name = 'lowkey'
    allowed_domains = ['https://madison.craigslist.org/']
    start_urls = ['http://https://madison.craigslist.org/d/jobs/search/jjj/']

    def parse(self, response):
        


    def parse_ad(self, response):
    

    rules = [
        LinkExtractor(
            allow=OpportunitiesItem.PAGINATION_REGEX,
            restrict_xpaths=OpportunitiesItem.PAGINATION_SELECTOR
        )
    ]