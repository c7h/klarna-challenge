import unittest
from klarnachallenge.functions import ackermann_wolfram 
from klarnachallenge.config import wolfram_id

class AaaSTestCase(unittest.TestCase):
    def test_ackermann_wolfram_small(self):
        res = ackermann_wolfram(3, 3, wolfram_id)     
        self.assertEqual(res, 61)

    def test_ackermann_wolfram_large(self):
        res = ackermann_wolfram(5, 3, wolfram_id)     
        self.assertEqual(res, None)
