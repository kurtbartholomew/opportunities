import unittest
import sys, os
sys.path.append(os.path.abspath('.'))

import tests.test_parse as parsing
import tests.test_utils as utils
import tests.test_persistence as persistence

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(parsing))
suite.addTests(loader.loadTestsFromModule(utils))
suite.addTests(loader.loadTestsFromModule(persistence))


runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)