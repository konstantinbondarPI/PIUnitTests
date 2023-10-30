import unittest
import time
from Example.CoveredCode import *


def timing_decorator(fun):
    def wrapped(*args, **kwargs):
        start_time = time.time()
        result = fun(*args, **kwargs)
        print(f"{fun.__name__} {(time.time() - start_time):.2f}")
        return result
    return wrapped


class CodeTestCase(unittest.TestCase):
    @timing_decorator
    def test_add_and_multiply(self) -> None:
        time.sleep(1)
        self.assertEqual(add_and_multiply(0, 1, 4, 5, add=10, multiply_by=2), [20, 22, 28, 30])

    @timing_decorator
    def test_divide(self):
        self.assertEqual(divide(3, 3), 1)
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(1, 2), 0.5)

        time.sleep(0.5)

        with self.assertRaises(ArithmeticError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Divide by 0")

