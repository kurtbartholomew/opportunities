import unittest

from opportunities.opportunities.persistence import db, models
from sqlalchemy.orm import sessionmaker

class PersistenceTest(unittest.TestCase):

    def setUp():
        eng = db(debug=True)
        Session = sessionmaker(bind=eng)
        self.session = Session()

    def test_adding_an_ad(self):
        self.session.add(
            models.Ad(
                category = 'Manual Labor',
                title = 'Make Cheese',
                date = '2018-05-30 09:09:09', 
                city = 'Madison',
                map_address_url = 'https://maps.google.com/?q=loc%3A+%37%30%38+%31%2F%34+East+Johnson+St+Madison+WI+US',
                ad_attributes = 'compensation: based on experience,employment: part-time,',
                ad_url = 'https://madison.craigslist.org/fbh/d/make-cheese/6602582230.html',
                ad_post = 'this is a cool job'
            )
        )

    def tearDown():
        self.session.commit()