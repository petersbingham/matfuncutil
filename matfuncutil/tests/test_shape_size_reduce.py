import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import unittest
import matfuncutil as mfc

class test(unittest.TestCase):

    def _runTest(self):
        dmat1 = mfc.dMat({0.:mfc.nw.matrix([[1,2],[3,4],[5,6]])})
        self.assertEqual(dmat1.valsize(),6)
        self.assertEqual(dmat1.valshape(),(3,2))

        vec1 = dmat1.create_reduced_dim(0)
        self.assertEqual(vec1.valsize(),2)
        self.assertEqual(vec1.valshape(),(1,2))
        mfc.nw.are_matrices_close(vec1[0][1],mfc.nw.vector([1,2]))

        vec2 = dmat1.create_reduced_dim(0, col=True)
        self.assertEqual(vec2.valsize(),3)
        self.assertEqual(vec2.valshape(),(3,1))
        mfc.nw.are_matrices_close(vec2[0][1],mfc.nw.vector([1,3,5]))

        dmat2 = mfc.dMat({0.:mfc.nw.matrix([[1,2],[3,4]])})
        vec3 = dmat2.create_reduced_dim(diag=True)
        self.assertEqual(vec3.valsize(),2)
        self.assertEqual(vec3.valshape(),(1,2))
        mfc.nw.are_matrices_close(vec3[0][1],mfc.nw.vector([1,4]))

        dsca = vec1.create_reduced_dim(0)
        self.assertEqual(dsca.valsize(),1)
        self.assertEqual(dsca.valshape(),(1,1))

    def runTest(self):
        mfc.use_python_types()
        self._runTest()
        mfc.use_mpmath_types()
        self._runTest()

if __name__ == "__main__":
    #Just for debug
    b = test()
    b.runTest()
