import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import pynumwrap as nw
from matfuncutil import discrete as dis
import dumMats
dis.nw.usePythonTypes()
dumMats.nw.usePythonTypes()

import unittest

class test_allUnitary(unittest.TestCase):
    def runTest(self):
        d = dumMats.twoUnitary()
        self.assertTrue(d.isUnitary())

class test_oneUnitary(unittest.TestCase):
    def runTest(self):
        d = dumMats.oneUnitary()
        self.assertFalse(d.isUnitary())

class test_noneUnitary(unittest.TestCase):
    def runTest(self):
        d = dumMats.noneUnitary()
        self.assertFalse(d.isUnitary())

class test_absolute(unittest.TestCase):
    def runTest(self):
        d = dumMats.getAbsoluteTest()
        d_abs = d.absolute()
        self.assertTrue(nw.areMatricesClose(d_abs[1.0],dumMats.getIdentity()))
        self.assertTrue(nw.areMatricesClose(d_abs[2.0],
                                            dumMats.getComplex1Absolute()))
        

if __name__ == "__main__":
    #Just for debug
    b = test_absolute()
    b.runTest()
