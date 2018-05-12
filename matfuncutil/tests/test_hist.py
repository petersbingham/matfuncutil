import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import matfuncutil as mfc

import math
import unittest

class test_history_numpy(unittest.TestCase):
    def runTest(self):
        mfc.use_python_types()
        cSin = mfc.cVal(math.sin)
        dSin = cSin.discretise(-6., 6., 200)
        dSin2 = dSin.create_reduced_length(10,190,20)
        self.assertEqual(dSin2.hist_str,"(-6e+00,6e+00,200)(10,182,9)")

class test_history_mpmath(unittest.TestCase):
    def runTest(self):
        mfc.use_mpmath_types()
        cSin = mfc.cVal(math.sin)
        dSin = cSin.discretise(-6., 6., 200)
        dSin2 = dSin.create_reduced_length(10,190,20)
        self.assertEqual(dSin2.hist_str,"(-6e+00,6e+00,200)(10,182,9)")

if __name__ == "__main__":
    #Just for debug
    b = test_history()
    b.runTest()
