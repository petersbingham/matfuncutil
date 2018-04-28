import copy
try:
    import sympy as sym
except:
    pass
from discrete import *
import pynumutil as nu

class cBase:
    def __init__(self, funPtr, units=None, sourceStr="", histStr="", 
                 chartTitle=""):
        self.funPtr = funPtr
        self.units = units
        self.sourceStr = sourceStr
        self.histStr = histStr
        self.chartTitle = chartTitle

    def isContinuous(self):
        return True

    def isDiscrete(self):
        return False

    def __call__(self, val):
        return self.funPtr(val)

    def discretise(self, startVal, endVal, numPoints):
        dcont = self._getDiscreteContainer()
        dcont.sourceStr = self.sourceStr
        hStr = "("+nu.sciStr(startVal)+","+nu.sciStr(endVal)
        hStr += ","+str(numPoints)+")"
        dcont.histStr = self.histStr + hStr
        sz = (endVal-startVal) / (numPoints-1)
        for i in range(numPoints):
            val = startVal +  sz*i
            dcont[val] = self.funPtr
        return dcont

    def _getDiscreteContainer(self):
        raise NotImplementedError

    def getSourceStr(self):
        return self.sourceStr

    def setSourceStr(self, sourceStr):
        self.sourceStr = sourceStr

    def getHistStr(self):
        if self.histStr == "":
            return "origin"
        return self.histStr

    def appendHistStr(self, histStr):
        if len(self.histStr) == 0:
            self.histStr = histStr
        else:
            self.histStr += "," + histStr

    def getCheckStr(self):
        return self.getHistStr()

    def setChartTitle(self, chartTitle):
        self.chartTitle = chartTitle

class cVal(cBase):
    def _getDiscreteContainer(self):
        return dVal(units=self.units)

    def findRoots(self):
        # TODO add generic root finder (eg pydelves)
        pass

class cVec(cBase):
    def _getDiscreteContainer(self):
        return dVec(units=self.units)

class cMat(cBase):
    def _getDiscreteContainer(self):
        return dMat(units=self.units)

    def determinant(self):
        # TODO Return a cVal that will evaluate self.funPtr and then find the
        # determiant automatically
        pass

class cPolyVal(cVal):
    def __init__(self, symVal, symVar, units=None, sourceStr=""):
        cVal.__init__(self, lambda val: nw.fromSympy(symVal.subs(symVar, val)),
                       units, sourceStr)
        self.symVal = symVal
        self.symVar = symVar

    def findRoots(self, **kwargs):
        var = sym.symbols(self.symVar)
        poly = sym.polys.Poly(self.symVal, var)
        kwargsCopy = copy.deepcopy(kwargs) # Copy because we may change
        if "nw_rootsSym" in kwargsCopy:
            if "symPoly_nroots" in kwargsCopy["nw_rootsSym"]:
                if "n" in kwargsCopy["nw_rootsSym"]["symPoly_nroots"] and \
                kwargsCopy["nw_rootsSym"]["symPoly_nroots"]["n"]=="dps":
                    kwargsCopy["nw_rootsSym"]["symPoly_nroots"]["n"] = nw.dps
            return nw.rootsSym(poly, **kwargsCopy["nw_rootsSym"])
        return nw.rootsSym(poly)

class cPolyMat(cMat):
    def __init__(self, symMat, symVar, units=None, sourceStr=""):
        cMat.__init__(self,
                       lambda val: nw.fromSympyMatrix(symMat.subs(symVar, val)),
                       units, sourceStr)
        self.symMat = symMat
        self.symVar = symVar

    def determinant(self, **kwargs):
        if "sym_matrix_det" in kwargs:
            det = self.symMat.det(**kwargs["sym_matrix_det"])
        else:
            det = self.symMat.det()
        return cPolyVal(det, self.symVar, self.units)
