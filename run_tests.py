import sys, os
sys.path.insert(0, os.path.join(os.path.abspath('.'), 'source/opportunities'))
import argparse

import unittest
import test.unit_tests.test_parse as parsing
import test.unit_tests.test_utils as utils
import test.unit_tests.test_persistence as persistence
import pdb

def run_unit_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(parsing))
    suite.addTests(loader.loadTestsFromModule(utils))
    suite.addTests(loader.loadTestsFromModule(persistence))

    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)

def run_functional_tests():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests for the scraper. (by default, unit tests are run)')
    parser.add_argument('-f','--functional', action="store_true", help='Runs functional tests')
    parser.add_argument('-a','--all', action="store_true", help='Runs unit and functional tests')
    args = parser.parse_args()
    
    if args.all:
        run_unit_tests()
        run_functional_tests()
    elif args.functional:
        run_functional_tests()
    else:
        run_unit_tests()