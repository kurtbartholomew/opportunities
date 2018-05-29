import unittest
import sys, os
sys.path.append(os.path.abspath('.'))

import tests.test_parse as parsing

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(parsing))


runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)