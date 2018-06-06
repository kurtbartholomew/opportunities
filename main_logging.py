import logging
import time
import pdb
from scrapy.utils.log import configure_logging
from logging.handlers import RotatingFileHandler

def configure_scrapy_log(path, log_level=logging.DEBUG):
    """Configure scrapy log output"""
    rotating_handler = RotatingFileHandler(path, maxBytes=1024000, backupCount=5)
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=log_level,
        handlers=[rotating_handler]
    )