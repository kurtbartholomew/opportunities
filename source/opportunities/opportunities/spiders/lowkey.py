# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

class LowkeySpider(scrapy.Spider):
    name = 'lowkey'
    allowed_domains = ['https://madison.craigslist.org/']
    start_urls = ['http://https://madison.craigslist.org/d/jobs/search/jjj/']

    def parse(self, response):
    
    def parse_titles(self, response):
    
    def parse_pages(self, response):

    rules = [
        # first rule, follow each job link
        # second rule, follow pagination links
    ]