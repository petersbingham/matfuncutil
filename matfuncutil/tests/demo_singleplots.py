import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dum_mats

a = dum_mats.row_offset_col_gain_zeroimag()
a.plot()

b = a.create_reduced_dim(0)
b.set_chart_title("Test title")
b.plot(logx=True, logy=True)

c = b.create_reduced_dim(1)
c.set_chart_parameters(leg_prefix="Test", xsize=10, ysize=10)
c.plot(imag=True)

d = a.trace()
d.plot()

import math
cSin = dum_mats.mfc.cSca(math.sin)
dSin = cSin.discretise(-2*math.pi, 2*math.pi, 200)
dSin.plot()

dSin2 = dSin.create_reduced_length(-math.pi, math.pi, 20)
dSin2.plot()