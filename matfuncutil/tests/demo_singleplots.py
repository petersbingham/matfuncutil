import os
import sys
import shutil
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dum_mats

if os.path.isdir("charts"):
    shutil.rmtree("charts")
os.makedirs("charts")

a = dum_mats.row_offset_col_gain_zeroimag()
a.set_chart_title("Test title a")
a.plot(save_path=basedir+os.sep+"charts\\chart.png", add_axis_lmts=True)

b = a.create_reduced_dim(0)
b.set_chart_title("Test title b")
b.plot(logx=True, logy=True)

c = b.create_reduced_dim(1)
c.set_chart_parameters(leg_prefix="Test", xsize=10, ysize=10)
c.plot(imag=True)

d = a.trace()
d.plot()

import math
cSin = dum_mats.mfc.cSca(math.sin, x_units="Ux", y_units="Uy")
dSin = cSin.discretise(-2*math.pi, 2*math.pi, 200)
dSin.set_axis_labels("Ax", "Ay")
dSin.plot()

dSin2 = dSin.create_reduced_length(-math.pi, math.pi, 20)
dSin2.plot()