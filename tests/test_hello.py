import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from my_python_package.hello import print_hello
import logging

class TestHello(unittest.TestCase):
    def test_print_hello(self):
        with self.assertLogs(level='INFO') as log:
            print_hello()
            self.assertIn('Hello World', log.output[0])

if __name__ == '__main__':
    unittest.main()