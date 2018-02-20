import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dumMats
from scatteringutil import discrete as dis

import unittest

class test_convertUnits(unittest.TestCase):
    def runTest(self):
        d_ryd = dumMats.rowOffsetColGain_posNegImag()
        d_eV = d_ryd.convertUnits(dis.eVs)
        for val in zip(d_ryd.sortedKeys(), d_eV.sortedKeys()):
            self.assertAlmostEqual(val[0]*dis.con.RYD_to_EV, val[1])

if __name__ == "__main__":
    #Just for debug
    b = test_convertUnits()
    b.runTest()
