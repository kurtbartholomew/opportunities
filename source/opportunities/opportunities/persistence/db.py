from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import psycopg2
import sqlite3

import os
import pdb

class db_engine():

    db_instance = None

    def __init__(self, debug=None):
        CONFIG_OBJECT = {
            'drivername' : os.getenv('DB_DIALECT', 'postgresql'),
            'username' :  os.getenv('DB_USER', 'postgres'),
            'password' :  os.getenv('DB_PASS', 'postgres'),
            'host' :  os.getenv('DB_HOST', 'localhost'),
            'port' :  os.getenv('DB_PORT','5432'),
            'database' :  os.getenv('DB_NAME','kurt')
        }

        db_url = URL(**CONFIG_OBJECT)

        if debug:
            self.db_instance = create_engine('sqlite:///test.db')
        else:
            self.db_instance = create_engine(db_url)



