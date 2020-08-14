import unittest
import csv
import os

from klarnachallenge.functions import *

class SimpleTestCases(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(SimpleTestCases, self).__init__(*args, **kwargs)
        with open(os.path.abspath('test/fibonacci.csv'), 'r') as f:
            self.fibonacci = list(csv.reader(f))

    def test_fib_positive_01(self):
        """test fib_simple against validated list of fibonacci numbers"""
        for x in range(0, 500):
            r = fib_simple(x)
            self.assertEqual(r, int(self.fibonacci[x][0]),
                    "error with input %i" % x)

    def test_fib_negative(self):
        """test fibonacci against negavie inputs"""
        neg_progression = ((-7, 13), (-6, -8), (-5, 5), (-4, -3), (-2, -1), (-1, 1))
        for kv in neg_progression:
            self.assertEqual(fib_simple(kv[0]), kv[1])

    def test_ackermann_simple(self):
        r = ackermann_simple(2, 1)
        self.assertEqual(r, 5)

    def test_ackermann_simple_3_3(self):
        r = ackermann_simple(3, 3)
        self.assertEqual(r, 61)

    def test_ackermann_simple_5_3(self):
        """The simple function should exceed recursion depth"""
        self.assertRaises(RuntimeError, ackermann_simple, 5, 3)

    def test_factorial(self):
        r = factorial(10)
        self.assertEqual(r, 3628800)
