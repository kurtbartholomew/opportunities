from sqlalchemy import create_engine
import psycopg2
import sqlite3

import os

class db():

    db_instance = None

    def __init__(self, debug=None):
        # dialect = os.environ('DB_DIALECT') or 'postgresql'
        # driver = os.environ('DB_DRIVER') or 'psycopg2'
        # username =  os.environ('DB_USER') or 'kurt'
        # password =  os.environ('DB_PASS') or 'cuteducki3'
        # host =  os.environ('DB_HOST') or 'localhost'
        # port =  os.environ('DB_PORT') or ''
        # database =  os.environ('DB_NAME') or 'kurt'

        dialect = os.getenv('DB_DIALECT', 'postgresql')
        driver = os.getenv('DB_DRIVER', 'psycopg2')
        username =  os.getenv('DB_USER', 'kurt')
        password =  os.getenv('DB_PASS', 'cuteducki3')
        host =  os.getenv('DB_HOST', 'localhost')
        port =  os.getenv('DB_PORT','')
        database =  os.getenv('DB_NAME','kurt')

        if debug:
            self.db_instance = create_engine('sqlite:///opportunities.db')
        else:
            self.db_instance = create_engine(f'{dialect}+{driver}://{username}:{password}@{host}/{database}')



