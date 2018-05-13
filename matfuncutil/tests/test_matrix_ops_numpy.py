import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dum_mats
import unittest

class test_allUnitary(unittest.TestCase):
    def runTest(self):
        d = dum_mats.two_unitary()
        self.assertTrue(d.is_unitary())

class test_one_unitary(unittest.TestCase):
    def runTest(self):
        d = dum_mats.one_unitary()
        self.assertFalse(d.is_unitary())

class test_none_unitary(unittest.TestCase):
    def runTest(self):
        d = dum_mats.none_unitary()
        self.assertFalse(d.is_unitary())

class test_absolute(unittest.TestCase):
    def runTest(self):
        d = dum_mats.get_absolute_test()
        d_abs = d.absolute()
        self.assertTrue(dum_mats.mfc.nw.are_matrices_close(d_abs[1.0],
                                                        dum_mats.get_identity()))
        self.assertTrue(dum_mats.mfc.nw.are_matrices_close(d_abs[2.0],
                                                dum_mats.get_complex1_absolute()))
        

if __name__ == "__main__":
    #Just for debug
    b = test_absolute()
    b.runTest()
