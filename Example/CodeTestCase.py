import unittest
import time
from Example.CoveredCode import *

class CodeTestCase(unittest.TestCase):
    def test_add_and_multiply(self) -> None:
        time.sleep(1)
        self.assertEqual(add_and_multiply(0, 1, 4, 5, add=10, multiply_by=2), [20, 22, 28, 30])

    def test_divide(self):
        self.assertEqual(divide(3, 3), 1)
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(1, 2), 0.5)

        time.sleep(0.5)

        with self.assertRaises(ArithmeticError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Divide by 0")

