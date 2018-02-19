import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import random

import pynumwrap as nw

import conversions as con

RYDs = 0
eVs = 1

class disMats(dict):
    def __init__(self, units=RYDs):
        self.units = units
        
        self.chartTitle = ""
        self.colourCycle = ['red', 'green', 'blue', 'purple']
        self.legPrefix = ""
        self.useMarker = False
        self.xsize = None
        self.ysize = None
        
        self.sigFigs = 6
    
    def setChartParameters(self, chartTitle=None, colourCycle=None, 
                           legPrefix=None, useMarker=None, xsize=None, 
                           ysize=None):
        if chartTitle is not None:
            self.chartTitle = chartTitle
        if colourCycle is not None:
            self.colourCycle = colourCycle
        if legPrefix is not None:
            self.legPrefix = legPrefix
        if useMarker is not None:
            self.useMarker = useMarker
        if xsize is not None:
            self.xsize = xsize
        if ysize is not None:
            self.ysize = ysize
    
    def setPrintParameters(self, sigFigs):
        self.sigFigs = sigFigs

    def sortedKeys(self):
        return sorted(self.keys(),key=lambda x: x.real)

    def sortedValues(self):
        sortedValues = []
        for key in self.sortedKeys():
            sortedValues.append(self[key])
        return sortedValues
    
    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            key = self.sortedKeys()[key]
            return (key, dict.__getitem__(self, key))
        elif isinstance(key, slice):
            newKeys = self.sortedKeys()[key]
            newmat = self._initNewMat()
            for ene in newKeys:
                newmat[ene] = self[ene]
            return newmat 
        else:
            return dict.__getitem__(self, key)

    def calculateReductionIndices(self, startIndex, endIndex, numPoints, 
                                  fromEnd=False):
        if endIndex-startIndex+1 < numPoints:
            raise IndexError
        
        step = int((endIndex-startIndex) /(numPoints-1))
        if fromEnd:
            actStartIndex = startIndex+(endIndex-startIndex) - (numPoints-1)*step
            actEndIndex = endIndex
        else:
            actStartIndex = startIndex
            actEndIndex = startIndex+(numPoints-1)*step
            
        return (actStartIndex,actEndIndex+1,step),\
               (self.sortedKeys()[actStartIndex],self.sortedKeys()[actEndIndex])

    def __str__(self):
        string = ""
        fstr = '%.'+str(self.sigFigs)+'E'
        for ene in self.sortedKeys():
            if ene.imag == 0.:
                eneStr = fstr % ene.real
            elif ene.imag < 0:
                eneStr = fstr % ene.real + fstr % ene.imag+"i"
            else:
                eneStr = fstr % ene.real + "+" + fstr % ene.imag+"i"
            string += eneStr + ":\n" + str(self[ene]) + "\n\n"
        return string
    
    def convert(self, units):
        if units == self.units:
            return self
        elif self.units==RYDs or self.units==eVs:
            if units==RYDs:
                fac = 1./con.RYD_to_EV
            elif units==eVs:
                fac = con.RYD_to_EV
            else:
                raise("Unknown conversion")
        else:
            raise("Unknown conversion")
        newmat = self._initNewMat(units)
        for k,v in self.iteritems():
            newmat[k*fac] = v
        return newmat
    
    def plot(self, m, n, logx=False, logy=False, imag=False):
        self._initPlot()
        ls,ss = self.getPlotInfo_getElementPlotInfo(m, n, logx, logy, imag)
        plt.legend(ls, ss)
        plt.show()
    
    def plotRow(self, m, logx=False, logy=False, imag=False):
        self._initPlot()
        ls,ss = self.getPlotInfo_row(m, logx, logy, imag)
        plt.legend(ls, ss)
        plt.show()
    
    def plotAll(self, logx=False, logy=False, imag=False):
        self._initPlot()
        ls,ss = self.getPlotInfo_all(logx, logy, imag)
        plt.legend(ls, ss)
        plt.show()
    
    def plotTrace(self, logx=False, logy=False, imag=False):
        self._initPlot()
        self.getPlotInfo_trace(logx, logy, imag)
        plt.show()
    
    def getPlotInfo_getElementPlotInfo(self, m, n, logx=False, logy=False, imag=False):
        ls = []
        ss = []
        l,s = self._getElementPlotInfo(m, n, logx, logy, imag)
        ls.append(l)
        ss.append(s)
        return (ls, ss)
    
    def getPlotInfo_row(self, m, logx=False, logy=False, imag=False):
        size = self._getSize()
        ls = []
        ss = []
        for n in range(size):
            l,s = self._getElementPlotInfo(m, n, logx, logy, imag)
            ls.append(l)
            ss.append(s)
        return (ls, ss)
    
    def getPlotInfo_all(self, logx=False, logy=False, imag=False):
        size = self._getSize()
        ls = []
        ss = []
        for m in range(size):
            for n in range(size):
                l,s = self._getElementPlotInfo(m, n, logx, logy, imag)
                ls.append(l)
                ss.append(s)
        return (ls, ss)
    
    def getPlotInfo_trace(self, logx=False, logy=False, imag=False):
        ls = []
        ss = []
        l,s = self._getTracePlotInfo(logx, logy, imag)
        ls.append(l)
        ss.append(s)
        return (ls, None)
    
    def _initPlot(self):
        fig = plt.figure()
        fig.suptitle(self.chartTitle)
        if self.xsize is not None and self.ysize is not None:
            fig.set_size_inches(self.xsize, self.ysize, forward=True)
        plt.gca().set_prop_cycle(cycler('color', self.colourCycle))

    def _getElementPlotInfo(self, m, n, logx, logy, imag):
        xs, ys = self._getElementPlotNums(m, n, imag)
        legStr = self.legPrefix + ": "+str(m)+","+str(n)
        return (self._getLineFromNums(xs, ys, logx, logy), legStr)

    def _getTracePlotInfo(self, logx, logy, imag):
        xs, ys = self._getTracePlotNums(imag)
        return (self._getLineFromNums(xs, ys, logx, logy), None)
        
    def _getElementPlotNums(self, m, n, imag):
        xs = np.ndarray((len(self),), dtype=float)
        ys = np.ndarray((len(self),), dtype=float)
        for i,ene in enumerate(self.sortedKeys()):
            xs[i] = ene.real
            if not imag:
                ys[i] = self[i][m,n].real
            else:
                ys[i] = self[i][m,n].imag
        return xs, ys
        
    def _getTracePlotNums(self, imag):
        xs = np.ndarray((len(self),), dtype=float)
        ys = np.ndarray((len(self),), dtype=float)
        for i,ene in enumerate(self.sortedKeys()):
            xs[i] = ene.real
            trace = nw.trace(self[i])
            if not imag:
                ys[i] = trace.real
            else:
                ys[i] = trace.imag
        return xs, ys

    def _getLineFromNums(self, xs, ys, logx, logy):
        if self.useMarker:
            ma = "x"
            li = "None"
        else:
            ma = None
            li = '-'
        if logx and logy:
            lne, = plt.loglog(xs, ys, linestyle=li, marker=ma, basex=10)
        elif logx:
            lne, = plt.semilogx(xs, ys, linestyle=li, marker=ma, basex=10)
        elif logy:
            lne, = plt.semilogy(xs, ys, linestyle=li, marker=ma, basey=10)
        else:
            lne, = plt.plot(xs, ys, linestyle=li, marker=ma)
        return lne
    
    def _initNewMat(self, units=None):
        if units is None:
            units = self.units
        newmat = disMats(units)
        newmat.setChartParameters(self.chartTitle, self.colourCycle, 
                                  self.legPrefix, self.useMarker)
        newmat.setPrintParameters(self.sigFigs)
        return newmat
    
    def _getSize(self):
        key = random.choice(self.keys())
        return nw.shape(self[key])[0] 
    