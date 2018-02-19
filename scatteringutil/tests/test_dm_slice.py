import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import pynumwrap as nw
import dumMats
from scatteringutil import discreteMatrices as dm

import unittest

class test_intElementAccess(unittest.TestCase):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_posNegImag()
        self.assertEqual(len(d1),21)
        sortedKeys = d1.sortedKeys()
        sortedVals = d1.sortedValues()
        for i in range(21):
            kv = d1[i]
            self.assertEqual(kv[0], sortedKeys[i])
            self.assertEqual(kv[1], sortedVals[i])

class sliceTestHelper(unittest.TestCase):
    def calPosNegImagEne(self, i):
        return float(i)-float(i)*1j
    def calPosNegImagSubMat(self, i):
        return nw.matrix([[float(i), 2*float(i)], 
                         [10+float(i), 10+2*float(i)]])
    def checkPosNegImagSub(self, d, sortedVals, i, i_off, val):
        actKey = float(i_off)-float(i_off)*1j
        actMat = self.calPosNegImagSubMat(i_off)
        self.assertEqual(val,actKey)
        self.assertEqual(sortedVals[i],actMat)
        self.assertEqual(d[val],actMat)

class test_complexElementAccess(sliceTestHelper):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_posNegImag()
        sortedKeys = d1.sortedKeys()
        sortedVals = d1.sortedValues()
        for i,val in enumerate(sortedKeys):
            i_off = i-10
            self.checkPosNegImagSub(d1, sortedVals, i, i_off, val)

class test_simpSlice(sliceTestHelper):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_posNegImag()
        d2 = d1[1:-1]
        self.assertEqual(len(d2),19)
        sortedKeys = d2.sortedKeys()
        sortedVals = d2.sortedValues()
        for i,val in enumerate(sortedKeys):
            i_off = i-9
            self.checkPosNegImagSub(d1, sortedVals, i, i_off, val)

class test_stepSlice(sliceTestHelper):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_posNegImag()
        d2 = d1[::2]
        self.assertEqual(len(d2),11)
        sortedKeys = d2.sortedKeys()
        sortedVals = d2.sortedValues()
        for i,val in enumerate(sortedKeys):
            i_off = i*2-10
            self.checkPosNegImagSub(d1, sortedVals, i, i_off, val)

class test_stepSliceRange(sliceTestHelper):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_posNegImag()
        d2 = d1[1:-1:2]
        self.assertEqual(len(d2),10)
        sortedKeys = d2.sortedKeys()
        sortedVals = d2.sortedValues()
        for i,val in enumerate(sortedKeys):
            i_off = i*2-9
            self.checkPosNegImagSub(d1, sortedVals, i, i_off, val)
        
class test_calculateReductionIndices(sliceTestHelper):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_posNegImag()

        ret = d1.calculateReductionIndices(0,20,3)
        self.assertEqual(ret[0],(0,21,10))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-10),
                                 self.calPosNegImagEne(10)))

        ret = d1.calculateReductionIndices(1,19,3)
        self.assertEqual(ret[0],(1,20,9))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-9),
                                 self.calPosNegImagEne(9)))

        ret = d1.calculateReductionIndices(0,20,4)
        self.assertEqual(ret[0],(0,19,6))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-10),
                                 self.calPosNegImagEne(8)))

        ret = d1.calculateReductionIndices(1,19,4)
        self.assertEqual(ret[0],(1,20,6))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-9),
                                 self.calPosNegImagEne(9)))

        ret = d1.calculateReductionIndices(0,20,10)
        self.assertEqual(ret[0],(0,19,2))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-10),
                                 self.calPosNegImagEne(8)))

        ret = d1.calculateReductionIndices(1,19,10)
        self.assertEqual(ret[0],(1,20,2))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-9),
                                 self.calPosNegImagEne(9)))

        ret = d1.calculateReductionIndices(2,19,10)
        self.assertEqual(ret[0],(2,12,1))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-8),
                                 self.calPosNegImagEne(1)))
        
class test_calculateReductionIndicesFromEnd(sliceTestHelper):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_posNegImag()

        ret = d1.calculateReductionIndices(0,20,3,True)
        self.assertEqual(ret[0],(0,21,10))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-10),
                                 self.calPosNegImagEne(10)))

        ret = d1.calculateReductionIndices(1,19,3,True)
        self.assertEqual(ret[0],(1,20,9))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-9),
                                 self.calPosNegImagEne(9)))

        ret = d1.calculateReductionIndices(0,20,4,True)
        self.assertEqual(ret[0],(2,21,6))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-8),
                                 self.calPosNegImagEne(10)))

        ret = d1.calculateReductionIndices(1,19,4,True)
        self.assertEqual(ret[0],(1,20,6))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-9),
                                 self.calPosNegImagEne(9)))

        ret = d1.calculateReductionIndices(0,20,10,True)
        self.assertEqual(ret[0],(2,21,2))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-8),
                                 self.calPosNegImagEne(10)))

        ret = d1.calculateReductionIndices(1,19,10,True)
        self.assertEqual(ret[0],(1,20,2))
        self.assertEqual(ret[1],(self.calPosNegImagEne(-9),
                                 self.calPosNegImagEne(9)))

        ret = d1.calculateReductionIndices(2,19,10,True)
        self.assertEqual(ret[0],(10,20,1))
        self.assertEqual(ret[1],(self.calPosNegImagEne(0),
                                 self.calPosNegImagEne(9)))


if __name__ == "__main__":
    #Just for debug
    b = test_stepSlice()
    b.runTest()
