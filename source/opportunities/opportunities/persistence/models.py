from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class Ad(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True)
    category = Column(String)
    title = Column(String)
    date = Column(String)
    city = Column(String)
    map_address_url = Column(String)
    ad_attributes = Column(String)
    ad_url = Column(String)
    ad_post = Column(String)

    def __repr__(self):
        return "<Ad(id='%d', category='%s', title='%s', date='%s', ad_url='%s')>" % (
            self.id, self.category, self.title, self.date, self.ad_url
        )
    

