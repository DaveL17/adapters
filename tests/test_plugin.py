"""

"""
from shared.classes import APIBase # noqa
import shared.utils
import simpleeval  # noqa


# ===================================== simpleeval.py =====================================
class TestSimpleEval(APIBase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_simple_eval(self):
        """ Test simple evaluation """
        # ===================================== random_int() =====================================
        self.assertTrue(simpleeval.random_int(10) <= 10, "Method return should be less than input")
        self.assertTrue(simpleeval.random_int(100) <= 100, "Method return should be less than input")

        # ===================================== safe_power() =====================================
        self.assertEqual(simpleeval.safe_power(2, 4), 16, "Method didn't return the expected value.")

        # ===================================== safe_multi() =====================================
        self.assertEqual(simpleeval.safe_mult(10, "*"), "**********", "Method didn't return the expected value.")
        self.assertEqual(simpleeval.safe_mult(10, 2), 20, "Method didn't return the expected value.")

        # ===================================== safe_add() =====================================
        self.assertEqual(simpleeval.safe_add("**", "**"), "****", "Method didn't return the expected value.")
        self.assertEqual(simpleeval.safe_add(1, 1), 2, "Method didn't return the expected value.")

        # ===================================== simple_eval() =====================================
        self.assertEqual(simpleeval.simple_eval('x', None, None, {'x': 50}), 50, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x + 2', None, None, {'x': 50}), 52, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x - 2', None, None, {'x': 50}), 48, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x * 2', None, None, {'x': 50}), 100, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x / 2', None, None, {'x': 50}), 25, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x + 20 - (10 * 7)', None, None, {'x': 50}), 0, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('x ** 2', None, None, {'x': 5}), 25, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 2}), 1, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 3}), -1, "Method didn't return the expected value.")
        self.assertEqual(simpleeval.simple_eval('1 if x == 2 else -1 if x == 3 else 0', None, None, {'x': 4}), 0, "Method didn't return the expected value.")


class TestSomethingElse(APIBase):

    @classmethod
    def setUpClass(cls):
        pass
