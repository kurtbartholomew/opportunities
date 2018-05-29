import unittest
import sys, os
sys.path.append(os.path.abspath('.'))

import tests.test_parse as parsing
import tests.test_utils as utils

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(parsing))
suite.addTests(loader.loadTestsFromModule(utils))


runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)