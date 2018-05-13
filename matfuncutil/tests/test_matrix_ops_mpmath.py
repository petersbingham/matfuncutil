import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dum_mats
import unittest

def use_mpmath_types():
    dum_mats.mfc.use_mpmath_types()

def use_python_types():
    dum_mats.mfc.use_python_types()

class test_all_unitary(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dum_mats.two_unitary()
        self.assertTrue(d.is_unitary())
        use_python_types()

class test_one_unitary(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dum_mats.one_unitary()
        self.assertFalse(d.is_unitary())
        use_python_types()

class test_none_unitary(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dum_mats.none_unitary()
        self.assertFalse(d.is_unitary())
        use_python_types()

class test_absolute(unittest.TestCase):
    def runTest(self):
        use_mpmath_types()
        d = dum_mats.get_absolute_test()
        d_abs = d.absolute()
        self.assertTrue(dum_mats.mfc.nw.are_matrices_close(d_abs[1.0],
                                                        dum_mats.get_identity()))
        self.assertTrue(dum_mats.mfc.nw.are_matrices_close(d_abs[2.0],
                                                dum_mats.get_complex1_absolute()))
        use_python_types()

if __name__ == "__main__":
    #Just for debug
    b = test_all_unitary()
    b.runTest()
