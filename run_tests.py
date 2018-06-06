import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('.'), 'source/opportunities'))
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'source/opportunities/opportunities'))

import argparse
import unittest
import test.unit_tests.test_parse as parsing
import test.unit_tests.test_utils as utils
import test.unit_tests.test_persistence as persistence
import test.functional_tests.test as func_test
import test.unit_tests.test_middleware as middleware
import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from main_logging import configure_scrapy_log

configure_scrapy_log('logs/test_opportunities.log')
os.environ['SCRAPY_SETTINGS_MODULE'] = 'opportunities.settings'

# TODO: Think of a better way to inject template file dependencies
# that project uses to test scraping parsers
TEMPLATE_FILES = [
    {
        'name': 'SEARCH_TEMPLATE_FILE',
        'path': 'source/opportunities/test/templates/main_search.html',
        'url': 'https://madison.craigslist.org/d/jobs/search/jjj/' 
    }
]

def prepare_templates_for_tests(template_files):
    def _resolve_path(path):
        return os.path.abspath(path)

    def _retrieve_if_not_present(template):
        path = _resolve_path(template['path'])
        up_to_date = False
        res = None
        if os.path.isfile(path):
            stats = os.stat(path)
            if datetime.now().day == datetime.fromtimestamp(stats.st_mtime).day:
                up_to_date = True
        
        if not up_to_date:
            res = requests.get(template['url'])
            with open(path, 'w') as search:
                search.write(res.text)

    try: 
        for template_file in template_files:
            _retrieve_if_not_present(template_file)
    except ConnectionError as error:
        logging.error('Unable to retrieve html from url due to error')
        logging.error(error)
        sys.exit(1)

def add_unit_tests(suite, loader):
    suite.addTests(loader.loadTestsFromModule(parsing))
    suite.addTests(loader.loadTestsFromModule(utils))
    suite.addTests(loader.loadTestsFromModule(middleware))

def add_functional_tests(suite, loader):
    suite.addTests(loader.loadTestsFromModule(persistence))
    suite.addTests(loader.loadTestsFromModule(func_test))

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run tests for the scraper. (by default, unit tests are run)')
    parser.add_argument('-f','--functional', action="store_true", help='Runs functional tests')
    parser.add_argument('-a','--all', action="store_true", help='Runs unit and functional tests')
    return parser.parse_args()

def run_tests(arguments):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if arguments.all:
        add_unit_tests(suite, loader)
        add_functional_tests(suite, loader)
    elif arguments.functional:
        add_functional_tests(suite, loader)
    else:
        add_unit_tests(suite, loader)
    
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

if __name__ == '__main__':
    
    arguments = parse_arguments()
    prepare_templates_for_tests(TEMPLATE_FILES)
    run_tests(arguments)
