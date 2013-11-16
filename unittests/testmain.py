import unittest
import testpyimage
import handranktest
from handrank import *
from handgen import *

suite = unittest.TestSuite()
suite.addTest(handranktest.HandRankingTest("test_main"))
suite.addTest(handranktest.HandCompareTest("test_main"))
#suite.addTest(testpyimage.PyImageTest("testmain"))
runner = unittest.TextTestRunner()
runner.run(suite)
