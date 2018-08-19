from continuous import *
from matfuncutil.release import __version__

def use_python_types():
    nw.use_python_types()

def use_mpmath_types(dps=nw.dps_default_mpmath):
    nw.use_mpmath_types(dps)

def set_type_mode(mode, dps=None):
    nw.set_type_mode(mode, dps)
