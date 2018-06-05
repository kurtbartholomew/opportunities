from opportunities.pipelines import OpportunitiesPipeline
from opportunities.persistence.db import Database
from opportunities.persistence.models import Ad
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String

class TestOpportunitiesPipeline(OpportunitiesPipeline):
    def __init__(self):
        db = Database(config={'database':'test_opportunities'})
        engine = db.get_engine()
        Ad.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()