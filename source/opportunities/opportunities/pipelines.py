# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from persistence import db, models
from sqlalchemy.orm import sessionmaker

class OpportunitiesPipeline(object):
    def __init__(self):
        eng = db()
        Session = sessionmaker(bind=eng.db_instance)
        self.session = Session()

    def process_item(self, item, spider):
        # pdb.set_trace()
        ad = models.Ad(
            category = item.get('category'),
            title = item.get('title'), 
            date = item.get('date'), 
            city = item.get('city'),
            map_address_url = item.get('map_address_url'),
            ad_attributes = item.get('ad_attributes'),
            ad_url = item.get('ad_url'),
            ad_post = item.get('ad_post')
        )
        self.session.add(ad)
        self.session.commit()
        return item
