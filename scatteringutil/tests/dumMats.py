import numpy as np

import pynumwrap as nw

from scatteringutil import discreteMatrices as dm

def rowOffsetColGain_zeroImag(sz=100):
    d = dm.disMats()
    for i in range(sz):
        d[float(i)] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d

def rowOffsetColGain_posImag(sz=100):
    d = dm.disMats()
    for i in range(sz):
        d[float(i)+1j] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d

def rowOffsetColGain_negImag(sz=100):
    d = dm.disMats()
    for i in range(sz):
        d[float(i)-1j] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d

def rowOffsetColGain_posNegImag(rg=10):
    d = dm.disMats()
    for i in range(-rg,rg+1):
        d[float(i)-float(i)*1j] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d