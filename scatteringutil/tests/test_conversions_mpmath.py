import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import pynumwrap as nw
import dumMats

import unittest

class test_StoT(unittest.TestCase):
    def runTest(self):
        d1 = dumMats.rowOffsetColGain_zeroImag_Smat()
        d1.toDisTMats()

if __name__ == "__main__":
    #Just for debug
    b = test_StoT()
    b.runTest()
