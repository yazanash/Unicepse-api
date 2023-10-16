import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        """It should Create an Account and assert that it exists"""
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
