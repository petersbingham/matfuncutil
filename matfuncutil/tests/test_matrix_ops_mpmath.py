import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dumMats
import unittest

def use_mpmath_types():
    dumMats.mfc.use_mpmath_types()

def use_python_types():
    dumMats.mfc.use_python_types()

class test_all_unitary(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dumMats.two_unitary()
        self.assertTrue(d.is_unitary())
        use_python_types()

class test_one_unitary(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dumMats.one_unitary()
        self.assertFalse(d.is_unitary())
        use_python_types()

class test_none_unitary(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dumMats.none_unitary()
        self.assertFalse(d.is_unitary())
        use_python_types()

class test_absolute(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dumMats.get_absolute_test()
        d_abs = d.absolute()
        self.assertTrue(dumMats.mfc.nw.are_matrices_close(d_abs[1.0],
                                                        dumMats.get_identity()))
        self.assertTrue(dumMats.mfc.nw.are_matrices_close(d_abs[2.0],
                                                dumMats.get_complex1_absolute()))
        use_python_types()

if __name__ == "__main__":
    #Just for debug
    b = test_all_unitary()
    b.runTest()
