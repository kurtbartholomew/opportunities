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
        
        ads = Selector(response).xpath(OpportunitiesItem.ITEM_SELECTOR)

        for ad in ads:
            item = OpportunitiesItem()
            item.title = ad.xpath(OpportunitiesItem.TITLE_SELECTOR).extract()
            item.date = ad.xpath(OpportunitiesItem.DATE_SELECTOR).extract()
            url = ad.xpath(OpportunitiesItem.URL_SELECTOR).extract()
            # TODO: Add filters here
            # if title does not include filter items
            yield scrapy.Request(url, self.parse_ad)
    


    def parse_ad(self, response):
        ad = Selector(response)

        item = AdItem()
        item.category = ad.xpath(AdItem.CATEGORY_SELECTOR).extract()
        item.ad_post = ad.xpath(AdItem.AD_POST_SELECTOR).extract()
        main_section = ad.xpath(AdItem.AD_BODY_PARENT_SELECTOR)
        item.title = main_section.xpath(AdItem.TITLE_SELECTOR).extract()
        item.city = main_section.xpath(AdItem.AD_CITY_SELECTOR).extract()

        # TODO: Parse date string into datetime object
        item.date = main_section.xpath(AdItem.DATE_SELECTOR).extract()
        item.map_address_url = main_section.xpath(AdItem.MAP_ADDRESS_SELECTOR).extract()

        # TODO: Factor out into clean method and handle as items for seperate table
        # For now, just turning into a string delimited by commas
        attributes_keys = main_section.xpath(AdItem.AD_ATTRS_KEYS_SELECTOR) \
                                 .re(AdItem.Ad_ATTRS_REGEX)
        attributes_vals = main_section.xpath(AdItem.AD_ATTRS_VALS_SELECTOR).extract()
        attributes = ""
        for i, key in enumerate(attributes_keys):
            attributes += f'{key}: {attributes_vals[i]},'
        

        item.ad_url = response.url
        yield item
    

    rules = [
        LinkExtractor(
            allow=OpportunitiesItem.PAGINATION_REGEX,
            restrict_xpaths=OpportunitiesItem.PAGINATION_SELECTOR
        )
    ]