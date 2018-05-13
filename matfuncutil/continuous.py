import copy
try:
    import sympy as sym
except:
    pass
from discrete import *
import pynumutil as nu

class cBase:
    def __init__(self, fun_ref, units=None, source_str="", hist_str="", 
                 chart_title=""):
        self.fun_ref = fun_ref
        self.units = units
        self.source_str = source_str
        self.hist_str = hist_str
        self.chart_title = chart_title

    def is_continuous(self):
        return True

    def is_discrete(self):
        return False

    def __call__(self, val):
        return self.fun_ref(val)

    def discretise(self, start_val, end_val, num_points):
        dcont = self._get_discrete_container()
        dcont.source_str = self.source_str
        hStr = "("+nu.sci_str(start_val)+","+nu.sci_str(end_val)
        hStr += ","+str(num_points)+")"
        dcont.hist_str = self.hist_str + hStr
        sz = (end_val-start_val) / (num_points-1)
        for i in range(num_points):
            val = start_val +  sz*i
            dcont[val] = self.fun_ref
        return dcont

    def _get_discrete_container(self):
        raise NotImplementedError

    def get_source_str(self):
        return self.source_str

    def set_source_str(self, source_str):
        self.source_str = source_str

    def get_hist_str(self):
        if self.hist_str == "":
            return "origin"
        return self.hist_str

    def append_hist_str(self, hist_str):
        if len(self.hist_str) == 0:
            self.hist_str = hist_str
        else:
            self.hist_str += "," + hist_str

    def get_check_str(self):
        return self.get_hist_str()

    def set_chart_title(self, chart_title):
        self.chart_title = chart_title

class cVal(cBase):
    def _get_discrete_container(self):
        return dVal(units=self.units)

    def find_roots(self):
        # TODO add generic root finder (eg pydelves)
        pass

class cVec(cBase):
    def _get_discrete_container(self):
        return dVec(units=self.units)

class cMat(cBase):
    def _get_discrete_container(self):
        return dMat(units=self.units)

    def determinant(self):
        # TODO Return a cVal that will evaluate self.fun_ref and then find the
        # determiant automatically
        pass

class cPolyVal(cVal):
    def __init__(self, sym_val, sym_var, units=None, source_str=""):
        cVal.__init__(self, lambda val: nw.from_sympy(sym_val.subs(sym_var, val)),
                      units, source_str)
        self.sym_val = sym_val
        self.sym_var = sym_var

    def find_roots(self, **kwargs):
        var = sym.symbols(self.sym_var)
        poly = sym.polys.Poly(self.sym_val, var)
        kwargs_copy = copy.deepcopy(kwargs) # Copy because we may change
        if "nw_roots_sym" in kwargs_copy:
            if "symPoly_nroots" in kwargs_copy["nw_roots_sym"]:
                if "n" in kwargs_copy["nw_roots_sym"]["symPoly_nroots"] and \
                kwargs_copy["nw_roots_sym"]["symPoly_nroots"]["n"]=="dps":
                    kwargs_copy["nw_roots_sym"]["symPoly_nroots"]["n"] = nw.dps
            return nw.roots_sym(poly, **kwargs_copy["nw_roots_sym"])
        return nw.roots_sym(poly)

class cPolyMat(cMat):
    def __init__(self, sym_mat, sym_var, units=None, source_str=""):
        cMat.__init__(self,
                      lambda val: nw.from_sympy_matrix(sym_mat.subs(sym_var, val)),
                      units, source_str)
        self.sym_mat = sym_mat
        self.sym_var = sym_var

    def determinant(self, **kwargs):
        if "sym_matrix_det" in kwargs:
            det = self.sym_mat.det(**kwargs["sym_matrix_det"])
        else:
            det = self.sym_mat.det()
        return cPolyVal(det, self.sym_var, self.units)
