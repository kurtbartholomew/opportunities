# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from ..items import OpportunitiesItem, AdItem
from datetime import datetime, timedelta
import pytz
import pdb

search_page_date_time_format = '%Y-%m-%d %H:%M'
ad_page_date_time_format = '%Y-%m-%dT%H:%M:%S%z'

class LowkeySpider(Spider):
    name = 'lowkey'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://madison.craigslist.org/d/jobs/search/jjj/']

    def _convert_search_date_to_utc(self, local_datetime):
        central_tz = pytz.timezone('America/Chicago')
        applied_tz_datetime = central_tz.localize(local_datetime)
        return applied_tz_datetime.astimezone(pytz.utc)
    
    def _convert_ad_date_to_utc(self, localized_date_str):
        localized_date = datetime.strptime(localized_date_str, ad_page_date_time_format)
        utc_date = localized_date + localized_date.utcoffset()
        return utc_date

    # since utc transformation is not always perfect, fuzz the bounds of days a bit
    def _is_in_acceptable_time_range(self, utc_date):
        today = pytz.utc.localize(datetime.now())
        today_upper_bound = today + timedelta(hours=1)
        today_lower_bound = today - timedelta(hours=1)
        return today_lower_bound.day == utc_date.day or today_upper_bound.day == utc_date.day

    def parse(self, response):
        selector = Selector(response)
        ads = selector.xpath(OpportunitiesItem.ITEM_SELECTOR)

        for ad in ads:
            item = OpportunitiesItem()
            date_str = ad.xpath(OpportunitiesItem.DATE_SELECTOR).extract_first()
            date = datetime.strptime(date_str, search_page_date_time_format)
            utc_date = self._convert_search_date_to_utc(date)
            if self._is_in_acceptable_time_range(utc_date):
                url = ad.xpath(OpportunitiesItem.URL_SELECTOR).extract_first()
                yield scrapy.Request(url, self.parse_ad)
            else:
                raise CloseSpider("No more ads in current date range. Terminating now.")

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
        item['title'] = main_section.xpath(AdItem.TITLE_SELECTOR).extract_first().strip()
        item['city'] = main_section.xpath(AdItem.AD_CITY_SELECTOR).extract_first().strip(' ()')
        localized_date_str = main_section.xpath(AdItem.DATE_SELECTOR).extract_first()
        item['date'] = self._convert_ad_date_to_utc(localized_date_str)
        item['map_address_url'] = main_section.xpath(AdItem.MAP_ADDRESS_SELECTOR).extract_first()

        # TODO: Factor out into clean method and handle as items for seperate table
        # For now, just turning into a string delimited by commas
        attributes_keys = main_section.xpath(AdItem.AD_ATTRS_KEYS_SELECTOR) \
                                 .re(AdItem.AD_ATTRS_REGEX)
        attributes_vals = main_section.xpath(AdItem.AD_ATTRS_VALS_SELECTOR).extract()
        attributes = ""
        if len(attributes_keys) == len(attributes_vals):
            for i, key in enumerate(attributes_keys):
                attributes += f'{key}: {attributes_vals[i]},'

        item['ad_attributes'] = attributes

        item['ad_url'] = response.url
        yield item
    