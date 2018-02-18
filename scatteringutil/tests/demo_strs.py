import os
import sys
from __builtin__ import raw_input
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dumMats

d = dumMats.rowOffsetColGain_zeroImag()
print str(d)

raw_input("Any key to continue.")
d = dumMats.rowOffsetColGain_posImag()
print str(d)

raw_input("Any key to continue.")
d = dumMats.rowOffsetColGain_negImag()
print str(d)

raw_input("Any key to continue.")
d = dumMats.rowOffsetColGain_posNegImag()
print str(d)