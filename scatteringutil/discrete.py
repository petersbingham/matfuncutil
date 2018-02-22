import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import random

import pynumwrap as nw

import conversions as con

RYDs = 0
eVs = 1

class Base(dict):
    def __init__(self, d={}, units=RYDs):
        dict.__init__(self, d)
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
    
    #TODO __setitem__ to perform type checks.
    
    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            key = self.sortedKeys()[key]
            return (key, dict.__getitem__(self, key))
        elif isinstance(key, slice):
            newKeys = self.sortedKeys()[key]
            newItem = self._createNewItem()
            self._initNewItem(newItem)
            for ene in newKeys:
                newItem[ene] = self[ene]
            return newItem 
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
    
    def convertUnits(self, units):
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
        newItem = self._createNewItem(units)
        self._initNewItem(newItem)
        for k,v in self.iteritems():
            newItem[k*fac] = v
        return newItem

    #TODO Ability to append additional obects to combine in one plot.
    def plot(self, logx=False, logy=False, imag=False):
        self._initPlot()
        ls,ss = self.getPlotInfo(logx, logy, imag)
        if ss is not None:
            plt.legend(ls, ss)
        plt.show()

    def getPlotInfo(self, logx=False, logy=False, imag=False):
        ls,ss = self._getPlotInfo(logx, logy, imag)
        return (ls, ss)

    def _initPlot(self):
        fig = plt.figure()
        fig.suptitle(self.chartTitle)
        if self.xsize is not None and self.ysize is not None:
            fig.set_size_inches(self.xsize, self.ysize, forward=True)
        plt.gca().set_prop_cycle(cycler('color', self.colourCycle))

    def _getPlotInfo(self, logx, logy, imag):
        xss, yss = self._getPlotNums(imag)
        return (self._getPlotLineFromNums(xss, yss, logx, logy), self._getPlotLegends())
    
    def _getPlotLineFromNums(self, xss, yss, logx, logy):
        lnes = []
        for xs, ys in zip(xss, yss):
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
            lnes.append(lne)
        return lnes

    def _initNewItem(self, item, units=None):
        if units is None:
            units = self.units
        item.setChartParameters(self.chartTitle, self.colourCycle, 
                                  self.legPrefix, self.useMarker)
        item.setPrintParameters(self.sigFigs)
    

class vals(Base):
    def _getPlotNums(self, imag):
        xs = np.ndarray((len(self),), dtype=float)
        ys = np.ndarray((len(self),), dtype=float)
        for i,ene in enumerate(self.sortedKeys()):
            xs[i] = ene.real
            if not imag:
                ys[i] = self[i][1].real
            else:
                ys[i] = self[i][1].imag
        return [xs], [ys]

    def _getPlotLegends(self):
        return None

    def _createNewItem(self, units=None):
        if units is None:
            units = self.units
        return vals(units=units)


class vecs(Base):
    def reduce(self, n):
        newItem = vals(self.units)
        self._initNewItem(newItem)
        for k,v in self.iteritems():
            newItem[k] = v[n]
        return newItem

    def _getPlotNums(self, imag):
        xss = []
        yss = []
        size = self._getSize()
        for n in range(size):
            xs = np.ndarray((len(self),), dtype=float)
            ys = np.ndarray((len(self),), dtype=float)
            for i,ene in enumerate(self.sortedKeys()):
                xs[i] = ene.real
                if not imag:
                    ys[i] = self[i][1][n].real
                else:
                    ys[i] = self[i][1][n].imag
            xss.append(xs)
            yss.append(ys)
        return xss, yss

    def _getPlotLegends(self):
        legStrs = []
        size = self._getSize()
        for n in range(size):
            legStrs.append(self.legPrefix + ": "+str(n))
        return legStrs

    def _createNewItem(self, units=None):
        if units is None:
            units = self.units
        return vecs(units=units)
    
    def _getSize(self):
        key = random.choice(self.keys())
        return nw.shape(self[key])[0]


class mats(Base):
    def reduce(self, m):
        newItem = vecs(self.units)
        self._initNewItem(newItem)
        for k,v in self.iteritems():
            newItem[k] = nw.getVector(v,m)
        return newItem

    def trace(self):
        newItem = vals(self.units)
        self._initNewItem(newItem)
        for k,v in self.iteritems():
            newItem[k] = nw.trace(v)
        return newItem

    def _getPlotNums(self, imag):
        xss = []
        yss = []
        size = self._getSize()
        for m in range(size):
            for n in range(size):
                xs = np.ndarray((len(self),), dtype=float)
                ys = np.ndarray((len(self),), dtype=float)
                for i,ene in enumerate(self.sortedKeys()):
                    xs[i] = self[i][0].real
                    if not imag:
                        ys[i] = self[i][1][m,n].real
                    else:
                        ys[i] = self[i][1][m,n].imag
                xss.append(xs)
                yss.append(ys)
        return xss, yss

    def _getPlotLegends(self):
        legStrs = []
        size = self._getSize()
        for m in range(size):
            for n in range(size):
                legStrs.append(self.legPrefix + ": "+str(m)+","+str(n))
        return legStrs

    def _createNewItem(self, units=None):
        if units is None:
            units = self.units
        return mats(units=units)
    
    def _getSize(self):
        key = random.choice(self.keys())
        return nw.shape(self[key])[0]


class Smats(mats):
    def toTMats(self):
        newItem = self._createNewItem(self.units)
        self._initNewItem(newItem)
        for k,v in self.iteritems():
            newItem[k] = v - nw.identity(nw.shape(v)[0])
        return newItem
    def toKMats(self):
        raise NotImplementedError
    def toXSMats(self):
        raise NotImplementedError
    def toEPhaseMats(self):
        raise NotImplementedError
    def toUniOpMats(self):
        raise NotImplementedError

class Kmats(mats):
    def toTMats(self):
        raise NotImplementedError
    def toSMats(self):
        raise NotImplementedError
    def toXSMats(self):
        raise NotImplementedError

class Tmats(mats):
    def toSMats(self):
        raise NotImplementedError
    def toKMats(self):
        raise NotImplementedError
    def toXSMats(self):
        raise NotImplementedError
