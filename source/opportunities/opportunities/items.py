# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OpportunitiesItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()

    # selector for seperate ad items
    ITEM_SELECTOR = '//p[@class="result-info"]'
    # selector for title of ad
    TITLE_SELECTOR = 'a[contains(@class,"result-title")]/text()'
    # selector for date ad was posted (in format of YYYY-MM-DD HH:MM)
    DATE_SELECTOR = 'time[@class="result-date"]/@datetime'
    # selector for url for additional crawling
    URL_SELECTOR = 'a[contains(@class,"result-title")]/@href'
    # regex to restrict the links that the crawler will follow
    PAGINATION_REGEX = '.*search\/\w+.*'
    #  selector to restrict area crawler will look for links to follow
    PAGINATION_SELECTOR = '//span[@class="buttons"]/a[@class="button next"]/@href'


class AdItem(scrapy.Item):
    category = scrapy.Field()
    ad_post = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    date = scrapy.Field()
    map_address_url = scrapy.Field()
    ad_attributes = scrapy.Field()
    ad_url = scrapy.Field()

    # selector for ad category in header of page
    CATEGORY_SELECTOR = '//nav[@class="breadcrumbs-container"]/ul/li[@class="crumb category"]/p/a/text()'
    # selector for body of main ad text
    AD_POST_SELECTOR = '//section[@id="postingbody"]'

    # parent selector for most of ad
    AD_BODY_PARENT_SELECTOR = '//section[@class="body"]'

    # parent selector for ad header
    HEADER_SECTION_PARENT_SELECTOR = '//span[@class="postingtitletext"]'
    # selector for title of ad
    TITLE_SELECTOR = HEADER_SECTION_PARENT_SELECTOR + '/span[@id="titletextonly"]/text()'
    # selector for city of ad
    AD_CITY_SELECTOR = HEADER_SECTION_PARENT_SELECTOR + '/small/text()'

    # selector for date ad was posted (in format of YYYY-MM-DDTHH:MM:SS-MMMM)
    DATE_SELECTOR = '//p[@id="display-date"]/time/@datetime'
    # selector for address within map (if provided)
    MAP_ADDRESS_SELECTOR = '//p[@class="mapaddress"]/small/a/@href'

    # selector for attributes of job (compensation, employment type, etc.)
    AD_ATTRS_KEYS_SELECTOR = '//p[@class="attrgroup"]/span/text()'
    AD_ATTRS_VALS_SELECTOR = '//p[@class="attrgroup"]/span/b/text()'
    # regex to capture attribute keys properly
    AD_ATTRS_REGEX = '^\w*'
    


