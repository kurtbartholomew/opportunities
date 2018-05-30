# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class OpportunitiesPipeline(object):
    def __init__(self):
        self.conn = sqlite3.connect('opportunities.db')
        self.cur = self.cnn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS ads ( \
                            id integer PRIMARY KEY, \
                            category text, \
                            title text, \
                            date datetime, \
                            city, \
                            map_address_url text, \
                            ad_attributes text, \
                            ad_url text
        )
        self.cur.execute("DELETE FROM ADS")

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO ADS (category, title, date, city, ad_url, ad_attributes, ad_post) \
            values(?,?,?)",
            (
                item.get('category') or 'miscellaneous',
                item.get('title') or 'none',
                item.get('date') or 'none',
                item.get('city') or 'none',
                item.get('map_address_url') or 'none',
                item.get('ad_attributes') or 'none',
                item.get('ad_url') or 'none'
            )
        )
        return item
