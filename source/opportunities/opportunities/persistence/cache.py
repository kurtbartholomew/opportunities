import redis 
import os

DEFAULT_CONFIG_OBJECT = {
    'host': os.getenv('CACHE_HOST','localhost'),
    'port': os.getenv('CACHE_PORT','6379'),
    'password': os.getenv('CACHE_PASSWORD', '')
}

class Cache():

    _connection_instance = None

    def get_conn(self):
        return self._connection_instance

    def __init__(self):
        self._connection_instance = redis.Redis(**DEFAULT_CONFIG_OBJECT)