import unittest
import time

import CoveredCode

class CodeTestCase(unittest.TestCase):
    def test_add_and_multiply(self) -> None:
        time.sleep(1)
        self.assertEqual(CoveredCode.add_and_multiply(0, 1, 4, 5, add=10, multiply_by=2), [20, 22, 28, 30])

    def test_divide(self):
        self.assertEqual(CoveredCode.divide(3, 3), 1)
        self.assertEqual(CoveredCode.divide(10, 2), 5)
        self.assertEqual(CoveredCode.divide(1, 2), 0.5)

        time.sleep(0.5)

        with self.assertRaises(ArithmeticError) as context:
            CoveredCode.divide(10, 0)
        self.assertEqual(str(context.exception), "Divide by 0")


if __name__ == "__main__":
    unittest.main()
