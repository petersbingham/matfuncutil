import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dumMats

a = dumMats.rowOffsetColGain_zeroImag()
a.plot()

b = a.reduce(0)
b.setChartParameters(chartTitle="Test title")
b.plot(logx=True, logy=True)

c = b.reduce(1)
c.setChartParameters(legPrefix="Test", xsize=10, ysize=10)
c.plot(imag=True)

d = a.trace()
d.plot()