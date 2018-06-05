from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import psycopg2
import sqlite3

import os

class Database():

    _engine = None
    DEFAULT_CONFIG_OBJECT = {
        'drivername' : os.getenv('DB_DIALECT', 'postgresql'),
        'username' :  os.getenv('DB_USER', 'opp_creator'),
        'password' :  os.getenv('DB_PASS', 'postgres'),
        'host' :  os.getenv('DB_HOST', 'localhost'),
        'port' :  os.getenv('DB_PORT','5432'),
        'database' :  os.getenv('DB_NAME','opportunities')
    }

    def __init__(self, debug=None, config=None):
        CONFIG_OBJECT = self.DEFAULT_CONFIG_OBJECT.copy()
        if config and type(config) == dict:
            CONFIG_OBJECT.update(config)

        db_url = URL(**CONFIG_OBJECT)
        if debug:
            self._engine = create_engine('sqlite:///source/opportunities/test/test.db')
        else:
            self._engine = create_engine(db_url)
    
    def get_engine(self):
        return self._engine
    
    def get_conn(self):
        return self._engine.connect()



