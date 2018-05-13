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
        csin = mfc.cVal(math.sin)
        dsin = csin.discretise(-6., 6., 200)
        dsin2 = dsin.create_reduced_length(10,190,20)
        self.assertEqual(dsin2.hist_str,"(-6e+00,6e+00,200)(10,182,9)")

class test_history_mpmath(unittest.TestCase):
    def runTest(self):
        mfc.use_mpmath_types()
        csin = mfc.cVal(math.sin)
        dsin = csin.discretise(-6., 6., 200)
        dsin2 = dsin.create_reduced_length(10,190,20)
        self.assertEqual(dsin2.hist_str,"(-6e+00,6e+00,200)(10,182,9)")

if __name__ == "__main__":
    #Just for debug
    b = test_history()
    b.runTest()
