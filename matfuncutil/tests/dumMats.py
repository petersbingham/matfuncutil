import numpy as np

import pynumwrap as nw

from matfuncutil import discrete as dis

def rowOffsetColGain_zeroImag(sz=100):
    d = dis.mats()
    _rowOffsetColGain_zeroImag(d,sz)
    return d

def rowOffsetColGain_posImag(sz=100):
    d = dis.mats()
    _rowOffsetColGain_posImag(d,sz)
    return d

def rowOffsetColGain_negImag(sz=100):
    d = dis.mats()
    _rowOffsetColGain_negImag(d,sz)
    return d

def rowOffsetColGain_posNegImag(rg=10):
    d = dis.mats()
    _rowOffsetColGain_posNegImag(d,rg)
    return d



def rowOffsetColGain_zeroImag_Smat(sz=100):
    d = dis.Smats()
    _rowOffsetColGain_zeroImag(d,sz)
    return d


def _rowOffsetColGain_zeroImag(d, sz):
    for i in range(sz):
        d[float(i)] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d

def _rowOffsetColGain_posImag(d, sz):
    for i in range(sz):
        d[float(i)+1j] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d

def _rowOffsetColGain_negImag(d, sz):
    for i in range(sz):
        d[float(i)-1j] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d

def _rowOffsetColGain_posNegImag(d, rg):
    for i in range(-rg,rg+1):
        d[float(i)-float(i)*1j] = nw.matrix([[float(i), 2*float(i)], 
                                 [10+float(i), 10+2*float(i)]])
    return d

def _getUniMat():
    return nw.matrix([[pow(2.,-.5), pow(2.,-.5),0], 
                      [-pow(2.,-.5)*1.j, pow(2.,-.5)*1.j,0],
                      [0, 0,1.j]])

def _getNonUniMat():
    return nw.matrix([[pow(3.,-.5), pow(2.,-.5),0], 
                      [-pow(2.,-.5)*1.j, pow(3.,-.5)*1.j,0],
                      [0, 0,1.j]])

def twoUnitary():
    d = dis.mats()
    d[1.0] = _getUniMat()
    d[2.0] = _getUniMat()
    return d

def oneUnitary():
    d = dis.mats()
    d[1.0] = _getUniMat()
    d[2.0] = _getNonUniMat()
    return d

def noneUnitary():
    d = dis.mats()
    d[1.0] = _getNonUniMat()
    d[2.0] = _getNonUniMat()
    return d

def getIdentity():
    return nw.matrix([[1., 1.], 
                      [1., 1.]])

def _getComplex1():
    return nw.matrix([[1.+1.j, 2.+2.j], 
                      [3.+3.j, 4.+4.j]])

def getComplex1Absolute():
    return nw.matrix([[1.4142135623730950488016887242097, 2.8284271247461900976033774484194], 
                      [4.2426406871192851464050661726291, 5.6568542494923801952067548968388]])

def getAbsoluteTest():
    d = dis.mats()
    d[1.0] = getIdentity()
    d[2.0] = _getComplex1()
    return d
