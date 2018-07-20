import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import unittest
import matfuncutil as mfc

class test_dVec(unittest.TestCase):
    def _assert_matrices_close(self, a, b):
        self.assertTrue(mfc.nw.are_matrices_close(a,b))
    
    def runTest(self):
        dVec = mfc.dVec()
        dVec[0.] = mfc.nw.vector([1.,1.j,1.+1.j])
        dVec[1.] = mfc.nw.vector([2.,2.j,2.+2.j])
        dVec[2.] = mfc.nw.vector([4.,4.j,4.+4.j])
        dVec_diff = dVec.gradient()
        self._assert_matrices_close(dVec_diff[0.],[1.+0.j, 1.j, 1.+1.j])
        self._assert_matrices_close(dVec_diff[1.],[1.5+0.j, 1.5j, 1.5+1.5j])
        self._assert_matrices_close(dVec_diff[2.],[2.+0.j, 2.j, 2.+2.j])

class test_dMat(unittest.TestCase):
    def _assert_matrices_close(self, a, b):
        self.assertTrue(mfc.nw.are_matrices_close(a,b))
    
    def runTest(self):
        dMat = mfc.dMat()
        dMat[0.] = mfc.nw.matrix([[1.,1.j],[2.,2.j]])
        dMat[1.] = mfc.nw.matrix([[2.,2.j],[4.,4.j]])
        dMat[2.] = mfc.nw.matrix([[4.,4.j],[8.,8.j]])
        dMat_diff = dMat.gradient()
        self._assert_matrices_close(dMat_diff[0.],[[1.,1.j],[2.,2.j]])
        self._assert_matrices_close(dMat_diff[1.],[[1.5,1.5j],[3.,3.j]])
        self._assert_matrices_close(dMat_diff[2.],[[2.,2.j],[4.,4.j]])

if __name__ == "__main__":
    #Just for debug
    b = test_dVec()
    b.runTest()
