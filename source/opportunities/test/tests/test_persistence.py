import unittest

from opportunities.opportunities.persistence import db
from opportunities.opportunities.persistence.models import Ad
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String

import pdb

class PersistenceTest(unittest.TestCase):

    def setUp(self):
        eng = db.db_engine(debug=True)
        self.engine = eng.db_instance
        Ad.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_adding_an_ad(self):
        test_ad = Ad(
                category = 'Manual Labor',
                title = 'Make Cheese',
                date = '2018-05-30 09:09:09', 
                city = 'Madison',
                map_address_url = 'https://maps.google.com/?q=loc%3A+%37%30%38+%31%2F%34+East+Johnson+St+Madison+WI+US',
                ad_attributes = 'compensation: based on experience,employment: part-time,',
                ad_url = 'https://madison.craigslist.org/fbh/d/make-cheese/6602582230.html',
                ad_post = 'this is a cool job'
            )
        self.session.add(test_ad)
        result = self.session.query(Ad).filter_by(title='Make Cheese').first()
        self.assertEqual(test_ad, result)
        self.session.rollback()

    def tearDown(self):
        Ad.__table__.drop(self.engine)
        self.session.close()
        self.engine.dispose()