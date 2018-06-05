# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pdb
from persistence.db import Database
from persistence.models import Ad
from sqlalchemy.orm import sessionmaker

class OpportunitiesPipeline(object):
    def __init__(self):
        db = Database()
        engine = db.get_engine()
        Ad.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        ad = Ad(
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
