import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dumMats
import unittest

def useMpmathTypes():
    dumMats.dis.nw.useMpmathTypes()

def usePythonTypes():
    dumMats.dis.nw.usePythonTypes()

class test_allUnitary(unittest.TestCase):
    def runTest(self):
        useMpmathTypes()
        d = dumMats.twoUnitary()
        self.assertTrue(d.isUnitary())
        usePythonTypes()

class test_oneUnitary(unittest.TestCase):
    def runTest(self):
        useMpmathTypes()
        d = dumMats.oneUnitary()
        self.assertFalse(d.isUnitary())
        usePythonTypes()

class test_noneUnitary(unittest.TestCase):
    def runTest(self):
        useMpmathTypes()
        d = dumMats.noneUnitary()
        self.assertFalse(d.isUnitary())
        usePythonTypes()

class test_absolute(unittest.TestCase):
    def runTest(self):
        useMpmathTypes()
        d = dumMats.getAbsoluteTest()
        d_abs = d.absolute()
        self.assertTrue(dumMats.dis.nw.areMatricesClose(d_abs[1.0],
                                                        dumMats.getIdentity()))
        self.assertTrue(dumMats.dis.nw.areMatricesClose(d_abs[2.0],
                                                dumMats.getComplex1Absolute()))
        usePythonTypes()

if __name__ == "__main__":
    #Just for debug
    b = test_allUnitary()
    b.runTest()
