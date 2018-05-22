import unittest
from StatusTest import StatusTest
from EventTest import EventTest
from FriendTest import FriendTest
from ProfileTest import ProfileTest

if __name__ == '__main__':
    test_cases = [StatusTest, EventTest, FriendTest, ProfileTest]

    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
