import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dumMats

a = dumMats.rowOffsetColGain_zeroImag()
a.plot()

b = a.createReducedDim(0)
b.setChartTitle("Test title")
b.plot(logx=True, logy=True)

c = b.createReducedDim(1)
c.setChartParameters(legPrefix="Test", xsize=10, ysize=10)
c.plot(imag=True)

d = a.trace()
d.plot()

import math
cSin = dumMats.mfc.cVal(math.sin)
dSin = cSin.discretise(-2*math.pi, 2*math.pi, 200)
dSin.plot()

dSin2 = dSin.createReducedSize(-math.pi, math.pi, 20)
dSin2.plot()