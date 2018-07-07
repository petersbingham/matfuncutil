import copy
try:
    import sympy as sym
except:
    pass
from discrete import *
import pynumutil as nu

class cBase:
    def __init__(self, fun_ref, x_units=None, y_units=None, chart_title="",
                 x_plotlbl="", y_plotlbl="", source_str=""):
        self.fun_ref = fun_ref
        self.x_units = x_units
        self.y_units = y_units
        self.chart_title = chart_title
        self.x_plotlbl = x_plotlbl
        self.y_plotlbl = y_plotlbl
        self.source_str = source_str
        self.hist_str = ""

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

    def set_axis_labels(self, x_plotlbl, y_plotlbl=""):
        self.x_plotlbl = x_plotlbl
        self.y_plotlbl = y_plotlbl

class cSca(cBase):
    def _get_discrete_container(self):
        return dSca({}, self.x_units, self.y_units, self.chart_title,
                    self.x_plotlbl, self.y_plotlbl, self.source_str)

    def find_roots(self):
        # TODO add generic root finder (eg pydelves)
        pass

class cVec(cBase):
    def _get_discrete_container(self):
        return dVec({}, self.x_units, self.y_units, self.chart_title,
                    self.x_plotlbl, self.y_plotlbl, self.source_str)

class cMat(cBase):
    def _get_discrete_container(self):
        return dMat({}, self.x_units, self.y_units, self.chart_title,
                    self.x_plotlbl, self.y_plotlbl, self.source_str)

    def determinant(self):
        # TODO Return a cSca that will evaluate self.fun_ref and then find the
        # determiant automatically
        pass

class cScaSympypoly(cSca):
    def __init__(self, sym_val, sym_var, x_units=None, y_units=None, 
                 chart_title="", x_plotlbl="", y_plotlbl="", source_str=""):
        cSca.__init__(self, lambda val: nw.from_sympy(sym_val.subs(sym_var, val)),
                      x_units, y_units, chart_title, x_plotlbl, y_plotlbl,
                      source_str)
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

class cMatSympypoly(cMat):
    def __init__(self, sym_mat, sym_var, x_units=None, y_units=None, 
                 chart_title="", x_plotlbl="", y_plotlbl="", source_str=""):
        cMat.__init__(self,
                      lambda val: nw.from_sympy_matrix(sym_mat.subs(sym_var, val)),
                      x_units, y_units, chart_title, x_plotlbl, y_plotlbl,
                      source_str)
        self.sym_mat = sym_mat
        self.sym_var = sym_var

    def determinant(self, **kwargs):
        # This speeds up that calculation. Also for large matrices calculation
        # never seems to complete within reasonable time:
        new_mat = nw.apply_fun_to_elements(self.sym_mat,
                                           lambda i,j,el: sym.poly(el))
        if "sym_matrix_det" in kwargs:
            det = new_mat.det(**kwargs["sym_matrix_det"])
        else:
            det = new_mat.det()
        return cScaSympypoly(det, self.sym_var, self.x_units, self.y_units,
                             self.chart_title, self.x_plotlbl, self.y_plotlbl,
                             self.source_str)
