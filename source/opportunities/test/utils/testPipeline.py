from opportunities.pipelines import OpportunitiesPipeline
from opportunities.persistence import db
from opportunities.persistence.models import Ad
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String

class TestOpportunitiesPipeline(OpportunitiesPipeline):
    def __init__(self):
        eng = db.db_engine(config={'database':'test_opportunities'})
        engine = eng.db_instance
        Ad.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()