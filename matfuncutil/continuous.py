try:
    import sympy as sym
except:
    pass
from discrete import *

class cBase:
    def __init__(self, funPtr, units=None):
        self.funPtr = funPtr
        self.units = units
        
        self.typeMode = nw.mode
        self.typeDps = nw.dps

    def getMode(self):
        return self.typeMode

    def __call__(self, val):
        return self.funPtr(val)

    def discretise(self, startVal, endVal, steps):
        dcont = self._getDiscreteContainer()
        sz = (endVal-startVal) / steps
        for i in range(steps+1):
            val = startVal +  sz*i
            dcont[val] = self(val)
        return dcont

    def _getDiscreteContainer(self):
        raise NotImplementedError

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
    def __init__(self, symVal, symVar, units=None):
        cVal.__init__(self, lambda val: nw.fromSympy(symVal.subs(symVar, val)),
                       units)
        self.symVal = symVal
        self.symVar = symVar

    def findRoots(self, **kwargs):
        var = sym.symbols(self.symVar)
        poly = sym.polys.Poly(self.symVal, var)
        if "nw_rootsSym" in kwargs:
            if "symPoly_nroots" in kwargs["nw_rootsSym"]:
                if "n" in kwargs["nw_rootsSym"]["symPoly_nroots"] and \
                kwargs["nw_rootsSym"]["symPoly_nroots"]["n"]=="dps":
                    kwargs["nw_rootsSym"]["symPoly_nroots"]["n"] = self.typeDps
            return nw.rootsSym(poly, **kwargs["nw_rootsSym"])
        return nw.rootsSym(poly)

class cPolyMat(cMat):
    def __init__(self, symMat, symVar, units=None):
        cMat.__init__(self,
                       lambda val: nw.fromSympyMatrix(symMat.subs(symVar, val)),
                       units)
        self.symMat = symMat
        self.symVar = symVar

    def determinant(self, **kwargs):
        if "sym_matrix_det" in kwargs:
            det = self.symMat.det(**kwargs["sym_matrix_det"])
        else:
            det = self.symMat.det()
        return cPolyVal(det, self.symVar, self.units)


def usePythonTypes_c(dps=nw.dps_default_python):
    nw.usePythonTypes(dps)

def useMpmathTypes_c(dps=nw.dps_default_mpmath):
    nw.useMpmathTypes(dps)

def setTypeMode_c(mode, dps=None):
    if mode is None or mode == nw.mode_python:
        if dps is None:
            usePythonTypes_c(nw.dps_default_python)
        else:
            usePythonTypes_c(dps)
    else:
        if dps is None:
            useMpmathTypes_c(nw.dps_default_mpmath)
        else:
            useMpmathTypes_c(dps)
