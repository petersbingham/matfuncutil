import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import dumMats

d = dumMats.rowOffsetColGain_zeroImag()

d.plot(0,0)

d.setChartParameters(chartTitle="Test title")
d.plotRow(0)

d.setChartParameters(legPrefix="Test", xsize=10, ysize=10)
d.plotAll()

d.setChartParameters(colourCycle=['black'], useMarker=True)
d.plotTrace()