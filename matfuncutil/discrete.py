import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import random

import pynumwrap as nw

class dBase(dict, object):
    def __init__(self, d={}, units=None, sourceStr=""):
        dict.__init__(self, d)
        self.units = units
        
        self.chartTitle = ""
        self.colourCycle = ['green', 'blue', 'purple', 'red']
        self.legPrefix = ""
        self.useMarker = False
        self.xsize = None
        self.ysize = None
        
        self.sigFigs = 6
        self.sourceStr = sourceStr
        self.histStr = ""

    def isContinuous(self):
        return False

    def isDiscrete(self):
        return True

    def sortedKeys(self):
        return sorted(self.keys(),key=lambda x: x.real)

    def values(self):
        vals = []
        for key in self.keys():
            vals.append(self[key])
        return vals

    def sortedValues(self):
        sortedVals = []
        for key in self.sortedKeys():
            sortedVals.append(self[key])
        return sortedVals
    
    def getRange(self):
        keys = self.sortedKeys()
        return (keys[0], keys[-1])

    #TODO __setitem__ to perform type checks and update histStr

    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            key = self.sortedKeys()[key]
            return (key, self._getVal(key))
        elif isinstance(key, slice):
            newKeys = self.sortedKeys()[key]
            newItem = self._createNewItem()
            self._initNewItem(newItem)
            hStr = str(key).replace("slice","").replace(" ","")
            newItem.histStr = self.histStr + hStr
            for ene in newKeys:
                newItem[ene] = self[ene]
            return newItem 
        else:
            return self._getVal(key)

    def _getVal(self, key):
        val = dict.__getitem__(self, key)
        try:
            val = val(key)
            self[key] = val
        except TypeError:
            pass
        return val

    def getSliceIndices(self, start=None, end=None, numPoints=None, 
                        fromEnd=False):
        if start is None:
            start = 0
        if end is None:
            end = len(self) - 1    
        if isinstance(start, float):
            start = self._getNearestIndex(start)
        if isinstance(end, float):
            end = self._getNearestIndex(end)

        if end-start+1 < numPoints:
            raise IndexError

        step = int((end-start) /(numPoints-1))
        if fromEnd:
            actStartIndex = start+(end-start) - (numPoints-1)*step
            actEndIndex = end
        else:
            actStartIndex = start
            actEndIndex = start+(numPoints-1)*step

        return (actStartIndex,actEndIndex+1,step),\
               (self.sortedKeys()[actStartIndex],self.sortedKeys()[actEndIndex])

    def createReducedLength(self, start=None, end=None, numPoints=None, 
                            fromEnd=False, forceEnd=False):
        si = self.getSliceIndices(start, end, numPoints, fromEnd)[0]
        ret = self[si[0]:si[1]:si[2]]
        if forceEnd:
            kvp = self[-1]
            ret[kvp[0]] = kvp[1] 
        return ret

    def __str__(self):
        string = ""
        fstr = '%.'+str(self.sigFigs)+'E'
        for val in self.sortedKeys():
            if val.imag == 0.:
                valStr = fstr % val.real
            elif val.imag < 0:
                valStr = fstr % val.real + fstr % val.imag+"i"
            else:
                valStr = fstr % val.real + "+" + fstr % val.imag+"i"
            string += valStr + ":\n" + str(self[val]) + "\n\n"
        return string

    def getSourceStr(self):
        return self.sourceStr

    def getHistStr(self):
        if self.histStr == "":
            return "origin"
        return self.histStr

    def getCheckStr(self):
        keys = self.sortedKeys()
        ret = "Len: " + str(len(keys)) + "\n"
        if len(keys) > 2:
            mi = len(keys) / 2
            ret += self._getKeyValCheckStr(keys,0)
            ret += "\n" + self._getKeyValCheckStr(keys,mi)
            ret += "\n" + self._getKeyValCheckStr(keys,-1)
        elif len(keys) == 2:
            ret += self._getKeyValCheckStr(keys,0)
            ret += "\n" + self._getKeyValCheckStr(keys,-1)
        elif len(keys) == 1:
            ret += self._getKeyValCheckStr(keys,0)
        return ret

    def setChartTitle(self, chartTitle):
        self.chartTitle = chartTitle

    def getChartTitle(self):
        return self.chartTitle

    def setChartParameters(self, colourCycle=None, legPrefix=None, useMarker=None, 
                           xsize=None, ysize=None):
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

    def _getKeyValCheckStr(self, keys, i):
        return str(keys[i]) + ":\n" + str(self[keys[i]])

    def plot(self, logx=False, logy=False, imag=False, show=True, 
             fileName=None):
        p = self._plot(logx, logy, imag)
        if fileName is not None:
            p.savefig(fileName, bbox_inches='tight')
        if show:
            p.show()

    def _plot(self, logx=False, logy=False, imag=False):
        self._initPlot(imag)
        ls,ss = self.getPlotInfo(logx, logy, imag)
        if ss is not None:
            plt.legend(ls, ss)
        plt.xlabel(self.units, fontsize=12)
        return plt

    def getPlotInfo(self, logx=False, logy=False, imag=False):
        ls,ss = self._getPlotInfo(logx, logy, imag)
        return (ls, ss)

    def _initPlot(self, imag):
        fig = plt.figure(facecolor="white")
        if not imag:
            fig.suptitle(self.chartTitle)
        else:
            fig.suptitle(self.chartTitle + " imag")
        if self.xsize is not None and self.ysize is not None:
            fig.set_size_inches(self.xsize, self.ysize, forward=True)
        plt.gca().set_prop_cycle(cycler('color', self.colourCycle))

    def _getPlotInfo(self, logx, logy, imag):
        xss, yss = self._getPlotNums(imag)
        return (self._getPlotLineFromNums(xss, yss, logx, logy), 
                self._getPlotLegends())

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

    def _getNearestIndex(self, ene):
        laste = None
        for i,e in enumerate(self.sortedKeys()):
            if e >= ene:
                if laste is None or abs(ene-e) < abs(ene-laste):
                    return i
                else:
                    return i-1
            laste = e
        return i

    def _initNewItem(self, item):
        item.setChartParameters(self.colourCycle, self.legPrefix, self.useMarker)
        item.setPrintParameters(self.sigFigs)

    def _createNewItem(self, units=None, newType=None):
        if units is None:
            units = self.units
        if newType is None:
            newType = type(self)
        newItem = newType(units=units, sourceStr=self.sourceStr)
        return newItem


class dVal(dBase):
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


class dVec(dBase):
    def createReducedDim(self, j):
        newItem = self._getReductionContainer()
        self._initNewItem(newItem)
        newItem.setChartTitle(self.chartTitle + ", n="+str(j+1))
        for key in self:
            val = self[key] # force fun eval if relevant
            newItem[key] = val[j]
        return newItem

    def _getPlotNums(self, imag):
        xss = []
        yss = []
        size = self._getSize()
        for j in range(size):
            xs = np.ndarray((len(self),), dtype=float)
            ys = np.ndarray((len(self),), dtype=float)
            for key,ene in enumerate(self.sortedKeys()):
                xs[key] = ene.real
                if not imag:
                    ys[key] = self[key][1][j].real
                else:
                    ys[key] = self[key][1][j].imag
            xss.append(xs)
            yss.append(ys)
        return xss, yss

    def _getPlotLegends(self):
        legStrs = []
        size = self._getSize()
        for j in range(size):
            legStrs.append(self.legPrefix + ": "+str(j+1))
        return legStrs

    def _getSize(self):
        key = random.choice(self.keys())
        return nw.shape(self[key])[0]

    def _getReductionContainer(self):
        return dVal(units=self.units)

class dMat(dBase):
    def createReducedDim(self, i, isCol=False):
        newItem = self._getReductionContainer()
        self._initNewItem(newItem)
        newItem.setChartTitle(self.chartTitle + ", m="+str(i+1))
        for key in self:
            val = self[key] # force fun eval if relevant
            newItem[key] = nw.getVector(val,i,isCol)
        return newItem

    def trace(self):
        newItem = dVal(units=self.units)
        self._initNewItem(newItem)
        for key in self:
            val = self[key] # force fun eval if relevant
            newItem[key] = nw.trace(val)
        return newItem

    def absolute(self):
        newItem = dVal(units=self.units)
        self._initNewItem(newItem)
        for key in self:
            val = self[key] # force fun eval if relevant
            newItem[key] = nw.absolute(val)
        return newItem

    def unitaryOp(self):
        newItem = dMat(units=self.units)
        self._initNewItem(newItem)
        for key in self:
            val = self[key] # force fun eval if relevant
            newItem[key] = nw.transpose(nw.conjugate(val))
        return newItem

    def isUnitary(self, rtol=1e-05, atol=1e-08):
        for val in self.values():
            if not nw.isUnitary(val, rtol, atol):
                return False
        return True

    def _getPlotNums(self, imag):
        xss = []
        yss = []
        size = self._getSize()
        for i in range(size):
            for j in range(size):
                xs = np.ndarray((len(self),), dtype=float)
                ys = np.ndarray((len(self),), dtype=float)
                for key,ene in enumerate(self.sortedKeys()):
                    xs[key] = self[key][0].real
                    if not imag:
                        ys[key] = self[key][1][i,j].real
                    else:
                        ys[key] = self[key][1][i,j].imag
                xss.append(xs)
                yss.append(ys)
        return xss, yss

    def _getPlotLegends(self):
        legStrs = []
        size = self._getSize()
        for i in range(size):
            for j in range(size):
                legStrs.append(self.legPrefix + ": "+str(i+1)+","+str(j+1))
        return legStrs

    def _getSize(self):
        key = random.choice(self.keys())
        return nw.shape(self[key])[0]

    def _getReductionContainer(self):
        return dVec(units=self.units)
