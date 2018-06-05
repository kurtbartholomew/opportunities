import unittest

from opportunities.persistence.db import Database
from opportunities.persistence.cache import Cache
from opportunities.persistence.models import Ad
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from datetime import datetime

class PersistenceTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        db = Database(debug=True)
        self.engine = db.get_engine()
        Ad.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        cache = Cache()
        self.cache_conn = cache.get_conn()

    @classmethod
    def tearDownClass(self):
        self.session.close_all()
        self.session.close()
        Ad.__table__.drop(self.engine)
        self.engine.dispose()
        self.cache_conn.flushall()
    
    def test_db_adding_an_ad(self):
        test_ad = Ad(
                category = 'Manual Labor',
                title = 'Make Cheese',
                date = datetime.utcnow(),
                city = 'Madison',
                map_address_url = 'https://maps.google.com/?q=loc%3A+%37%30%38+%31%2F%34+East+Johnson+St+Madison+WI+US',
                ad_attributes = 'compensation: based on experience,employment: part-time,',
                ad_url = 'https://madison.craigslist.org/fbh/d/make-cheese/6602582230.html',
                ad_post = 'this is a cool job'
            )
        self.session.add(test_ad)
        result = self.session.query(Ad).filter_by(title='Make Cheese').first()
        self.assertEqual(test_ad, result)
    
    def test_cache_adding_a_url(self):
        self.cache_conn.set('https://www.google.com', 1)
        res = self.cache_conn.get('https://www.google.com')
        self.assertNotEqual(res, None)

        