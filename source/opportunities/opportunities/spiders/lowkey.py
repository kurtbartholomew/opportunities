# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from ..items import OpportunitiesItem, AdItem
import pdb

# TODO Add current date here and do comparison in parse to capture only current date

class LowkeySpider(Spider):
    name = 'lowkey'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://madison.craigslist.org/d/jobs/search/jjj/']

    def parse(self, response):
        selector = Selector(response)
        ads = selector.xpath(OpportunitiesItem.ITEM_SELECTOR)

        for ad in ads:
            item = OpportunitiesItem()
            item['title'] = ad.xpath(OpportunitiesItem.TITLE_SELECTOR).extract_first()
            item['date'] = ad.xpath(OpportunitiesItem.DATE_SELECTOR).extract_first()
            url = ad.xpath(OpportunitiesItem.URL_SELECTOR).extract_first()
            # TODO: Add filters here
            # if title does not include filter items
            yield scrapy.Request(url, self.parse_ad)
        
        pagination_url = selector.xpath(OpportunitiesItem.PAGINATION_SELECTOR).extract_first()
        pagination_url = response.urljoin(pagination_url)
        yield scrapy.Request(pagination_url, self.parse)
    


    def parse_ad(self, response):
        ad = Selector(response)

        item = AdItem()
        item['category'] = ad.xpath(AdItem.CATEGORY_SELECTOR).extract_first()
        post_lines = ad.xpath(AdItem.AD_POST_SELECTOR).extract()
        item['ad_post'] = ''.join(post_lines)
        main_section = ad.xpath(AdItem.AD_BODY_PARENT_SELECTOR)
        item['title'] = main_section.xpath(AdItem.TITLE_SELECTOR).extract_first()
        item['city'] = main_section.xpath(AdItem.AD_CITY_SELECTOR).extract_first()

        # TODO: Parse date string into datetime object
        item['date'] = main_section.xpath(AdItem.DATE_SELECTOR).extract_first()
        item['map_address_url'] = main_section.xpath(AdItem.MAP_ADDRESS_SELECTOR).extract_first()

        # TODO: Factor out into clean method and handle as items for seperate table
        # For now, just turning into a string delimited by commas
        attributes_keys = main_section.xpath(AdItem.AD_ATTRS_KEYS_SELECTOR) \
                                 .re(AdItem.AD_ATTRS_REGEX)
        attributes_vals = main_section.xpath(AdItem.AD_ATTRS_VALS_SELECTOR).extract()
        attributes = ""
        for i, key in enumerate(attributes_keys):
            attributes += f'{key}: {attributes_vals[i]},'
        item['ad_attributes'] = attributes

        item['ad_url'] = response.url
        yield item
    