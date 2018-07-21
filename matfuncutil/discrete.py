import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import random

import pynumwrap as nw

class dBase(dict, object):
    def __init__(self, d=None, x_units=None, y_units=None, chart_title="",
                 x_plotlbl="", y_plotlbl="", source_str=""):
        if d is None:
            d = {}
        dict.__init__(self, d)
        self.x_units = x_units
        self.y_units = y_units
        
        self.chart_title = chart_title
        self.x_plotlbl = x_plotlbl
        self.y_plotlbl = y_plotlbl
        self.colour_cycle = ['black', 'purple', 'green', 'orange']
        self.leg_prefix = ""
        self.use_marker = False
        self.xsize = None
        self.ysize = None
        
        self.sig_figs = 6
        self.source_str = source_str
        self.hist_str = ""

    def is_continuous(self):
        return False

    def is_discrete(self):
        return True

    def sorted_keys(self):
        return sorted(self.keys(),key=lambda x: x.real)

    def values(self):
        vals = []
        for key in self.keys():
            vals.append(self[key])
        return vals

    def sorted_values(self):
        sorted_vals = []
        for key in self.sorted_keys():
            sorted_vals.append(self[key])
        return sorted_vals
    
    def get_range(self):
        keys = self.sorted_keys()
        return (keys[0], keys[-1])

    #TODO __setitem__ to perform type checks and update hist_str

    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            key = self.sorted_keys()[key]
            return (key, self._get_val(key))
        elif isinstance(key, slice):
            new_keys = self.sorted_keys()[key]
            new_item = self._create_new_item()
            self._init_new_item(new_item)
            hStr = str(key).replace("slice","").replace(" ","")
            new_item.hist_str = self.hist_str + hStr
            for ene in new_keys:
                new_item[ene] = self[ene]
            return new_item 
        else:
            return self._get_val(key)

    def _get_val(self, key):
        val = dict.__getitem__(self, key)
        try:
            val = val(key)
            self[key] = val
        except TypeError:
            pass
        return val

    def get_slice_indices(self, start=None, end=None, num_points=None, 
                          from_end=False):
        if start is None:
            start = 0
        if end is None:
            end = len(self) - 1    
        if isinstance(start, float):
            start = self._get_nearest_index(start)
        if isinstance(end, float):
            end = self._get_nearest_index(end)

        if end-start+1 < num_points:
            raise IndexError

        step = int((end-start) /(num_points-1))
        if from_end:
            act_start_index = start+(end-start) - (num_points-1)*step
            act_end_index = end
        else:
            act_start_index = start
            act_end_index = start+(num_points-1)*step

        return (act_start_index,act_end_index+1,step),\
               (self.sorted_keys()[act_start_index],self.sorted_keys()[act_end_index])

    def create_reduced_length(self, start=None, end=None, num_points=None, 
                              from_end=False, force_end=False):
        si = self.get_slice_indices(start, end, num_points, from_end)[0]
        ret = self[si[0]:si[1]:si[2]]
        if force_end:
            kvp = self[-1]
            ret[kvp[0]] = kvp[1] 
        return ret

    def __str__(self):
        string = ""
        fstr = '%.'+str(self.sig_figs)+'E'
        for val in self.sorted_keys():
            if val.imag == 0.:
                valstr = fstr % val.real
            elif val.imag < 0:
                valstr = fstr % val.real + fstr % val.imag+"i"
            else:
                valstr = fstr % val.real + "+" + fstr % val.imag+"i"
            string += valstr + ":\n" + str(self[val]) + "\n\n"
        return string

    def get_source_str(self):
        return self.source_str

    def get_hist_str(self):
        if self.hist_str == "":
            return "origin"
        return self.hist_str

    def get_check_str(self):
        keys = self.sorted_keys()
        ret = "Len: " + str(len(keys)) + "\n"
        if len(keys) > 2:
            mi = len(keys) / 2
            ret += self._get_key_val_check_str(keys,0)
            ret += "\n" + self._get_key_val_check_str(keys,mi)
            ret += "\n" + self._get_key_val_check_str(keys,-1)
        elif len(keys) == 2:
            ret += self._get_key_val_check_str(keys,0)
            ret += "\n" + self._get_key_val_check_str(keys,-1)
        elif len(keys) == 1:
            ret += self._get_key_val_check_str(keys,0)
        return ret

    def set_chart_title(self, chart_title):
        self.chart_title = chart_title

    def get_chart_title(self):
        return self.chart_title

    def supplement_chart_title(self, desc_str):
        self.chart_title += desc_str

    def set_axis_labels(self, x_plotlbl, y_plotlbl=""):
        self.x_plotlbl = x_plotlbl
        self.y_plotlbl = y_plotlbl

    def set_chart_parameters(self, colour_cycle=None, leg_prefix=None,
                             use_marker=None, xsize=None, ysize=None):
        if colour_cycle is not None:
            self.colour_cycle = colour_cycle
        if leg_prefix is not None:
            self.leg_prefix = leg_prefix
        if use_marker is not None:
            self.use_marker = use_marker
        if xsize is not None:
            self.xsize = xsize
        if ysize is not None:
            self.ysize = ysize

    def set_print_parameters(self, sig_figs):
        self.sig_figs = sig_figs

    def _get_key_val_check_str(self, keys, i):
        return str(keys[i]) + ":\n" + str(self[keys[i]])

    def plot(self, logx=False, logy=False, imag=False, show=True, 
             file_name=None):
        p = self._plot(logx, logy, imag)
        if file_name is not None:
            p.savefig(file_name, bbox_inches='tight')
        if show:
            p.show()

    def _set_axis_lbl(self, fun, units, plotlbl):
        if units is not None:
            if plotlbl == "":
                fun(units, fontsize=12)
            else:
                fun(plotlbl+" ("+units+")", fontsize=12)
        else:
            fun(plotlbl, fontsize=12)

    def _plot(self, logx=False, logy=False, imag=False):
        self._init_plot(imag)
        ls,ss = self.get_plot_info(logx, logy, imag)
        if ss is not None:
            plt.legend(ls, ss)
        self._set_axis_lbl(plt.xlabel, self.x_units, self.x_plotlbl)
        self._set_axis_lbl(plt.ylabel, self.y_units, self.y_plotlbl)
        return plt

    def get_plot_info(self, logx=False, logy=False, imag=False):
        ls,ss = self._get_plot_info(logx, logy, imag)
        return (ls, ss)

    def _init_plot(self, imag):
        fig = plt.figure(facecolor="white")
        if not imag:
            fig.suptitle(self.chart_title)
        else:
            fig.suptitle(self.chart_title + " imag")
        if self.xsize is not None and self.ysize is not None:
            fig.set_size_inches(self.xsize, self.ysize, forward=True)
        plt.gca().set_prop_cycle(cycler('color', self.colour_cycle))

    def _get_plot_info(self, logx, logy, imag):
        xss, yss = self._get_plot_nums(imag)
        return (self._get_plot_line_from_nums(xss, yss, logx, logy), 
                self._get_plot_legends())

    def _get_plot_line_from_nums(self, xss, yss, logx, logy):
        lnes = []
        for xs, ys in zip(xss, yss):
            if self.use_marker:
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

    def _get_nearest_index(self, ene):
        laste = None
        for i,e in enumerate(self.sorted_keys()):
            if e >= ene:
                if laste is None or abs(ene-e) < abs(ene-laste):
                    return i
                else:
                    return i-1
            laste = e
        return i

    def _init_new_item(self, item):
        # Nothing specific to the type of data here eg chart_title
        item.set_chart_parameters(self.colour_cycle, self.leg_prefix,
                                  self.use_marker)
        item.set_print_parameters(self.sig_figs)

    def _set_chart_title_for_new(self, new_item, add_title_str):
        new_item.set_chart_title(self.chart_title + add_title_str)

    def _create_new_item(self, x_units=None, y_units=None, new_type=None):
        if x_units is None:
            x_units = self.x_units
        if y_units is None:
            y_units = self.y_units
        if new_type is None:
            new_type = type(self)
        new_item = new_type({}, x_units, y_units, self.chart_title,
                            self.x_plotlbl, self.y_plotlbl, self.source_str)
        return new_item

    # These can be overridden in any derived classes.
    def _get_dSca(self):
        return dSca(x_units=self.x_units, source_str=self.source_str)
    def _get_dVec(self):
        return dVec(x_units=self.x_units, source_str=self.source_str)
    def _get_dMat(self):
        return dMat(x_units=self.x_units, source_str=self.source_str)


class dSca(dBase):
    def gradient(self):
        keys = self.sorted_keys()
        vals = self.sorted_values()
        grad = nw.gradient(vals, keys)
        new_item = self._get_dSca()
        self._set_chart_title_for_new(new_item, " gradient")
        for x in zip(keys,grad):
            new_item[x[0]] = x[1]
        return new_item

    def _get_plot_nums(self, imag):
        xs = np.ndarray((len(self),), dtype=float)
        ys = np.ndarray((len(self),), dtype=float)
        for i,ene in enumerate(self.sorted_keys()):
            xs[i] = ene.real
            if not imag:
                ys[i] = self[i][1].real
            else:
                ys[i] = self[i][1].imag
        return [xs], [ys]

    def _get_plot_legends(self):
        return None

class dVec(dBase):
    def create_reduced_dim(self, j):
        new_item = self._get_reduction_container()
        self._init_new_item(new_item)
        self._set_chart_title_for_new(new_item, " n="+str(j+1))
        for key in self:
            val = self[key] # force fun eval if relevant
            new_item[key] = val[j]
        return new_item

    def gradient(self):
        keys = self.sorted_keys()
        size = self._get_size()

        dSca_diffs = []
        for j in range(size):
            dSca_diffs.append(self.create_reduced_dim(j).gradient())

        new_item = self._get_dVec()
        self._set_chart_title_for_new(new_item, " gradient")
        for key in keys:
            new_item[key] = nw.vector([0.+0.j]*size)
            for j in range(size):
                new_item[key][j] = dSca_diffs[j][key]
        return new_item

    def _get_plot_nums(self, imag):
        xss = []
        yss = []
        size = self._get_size()
        for j in range(size):
            xs = np.ndarray((len(self),), dtype=float)
            ys = np.ndarray((len(self),), dtype=float)
            for key,ene in enumerate(self.sorted_keys()):
                xs[key] = ene.real
                if not imag:
                    ys[key] = self[key][1][j].real
                else:
                    ys[key] = self[key][1][j].imag
            xss.append(xs)
            yss.append(ys)
        return xss, yss

    def _get_plot_legends(self):
        leg_strs = []
        size = self._get_size()
        for j in range(size):
            leg_strs.append(self.leg_prefix + ": "+str(j+1))
        return leg_strs

    def _get_size(self):
        key = random.choice(self.keys())
        return nw.shape(self[key])[0]

    def _get_reduction_container(self):
        return dSca({}, self.x_units, self.y_units, self.chart_title,
                    self.x_plotlbl, self.y_plotlbl, self.source_str)

class dMat(dBase):
    def create_reduced_dim(self, i=0, col=False, diag=False):
        new_item = self._get_reduction_container()
        self._init_new_item(new_item)
        if not diag:
            self._set_chart_title_for_new(new_item, " m="+str(i+1))
        for key in self:
            val = self[key] # force fun eval if relevant
            if not diag:
                new_item[key] = nw.get_vector(val,i,col)
            else:
                new_item[key] = nw.get_diag(val)
        return new_item

    def trace(self):
        new_item = self._get_dSca()
        self._init_new_item(new_item)
        self._set_chart_title_for_new(new_item, " trace")
        for key in self:
            val = self[key] # force fun eval if relevant
            new_item[key] = nw.trace(val)
        return new_item

    def absolute(self):
        new_item = self._get_dSca()
        self._init_new_item(new_item)
        self._set_chart_title_for_new(new_item, " absolute")
        for key in self:
            val = self[key] # force fun eval if relevant
            new_item[key] = nw.absolute(val)
        return new_item

    def unitary_op(self):
        new_item = self._get_dMat()
        self._init_new_item(new_item)
        self._set_chart_title_for_new(new_item, " unitary op")
        for key in self:
            val = self[key] # force fun eval if relevant
            new_item[key] = nw.unitary_op(val)
        return new_item

    def diagonalise(self):
        new_item = self._get_dMat()
        self._init_new_item(new_item)
        self._set_chart_title_for_new(new_item, " diagonalised")
        for key in self:
            val = self[key] # force fun eval if relevant
            new_item[key] = nw.diagonalise(val)
        return new_item

    def eigenvalues(self):
        new_item = self._get_dVec()
        self._init_new_item(new_item)
        self._set_chart_title_for_new(new_item, " eigenvalues")
        for key in self:
            val = self[key] # force fun eval if relevant
            new_item[key] = nw.eigenvalues(val)
        return new_item

    def gradient(self):
        keys = self.sorted_keys()
        size = self._get_size()

        dVec_diffs = []
        for i in range(size):
            dVec_diffs.append(self.create_reduced_dim(i).gradient())

        new_item = self._get_dMat()
        self._set_chart_title_for_new(new_item, " gradient")
        for key in keys:
            new_item[key] = nw.matrix([[0.+0.j]*size]*size)
            for i in range(size):
                for j in range(size):
                    new_item[key][i,j] = dVec_diffs[i][key][j]
        return new_item

    def is_unitary(self, rtol=1e-05, atol=1e-08):
        for val in self.values():
            if not nw.is_unitary(val, rtol, atol):
                return False
        return True

    def _get_plot_nums(self, imag):
        xss = []
        yss = []
        size = self._get_size()
        for i in range(size):
            for j in range(size):
                xs = np.ndarray((len(self),), dtype=float)
                ys = np.ndarray((len(self),), dtype=float)
                for k in range(len(self)):
                    xs[k] = self[k][0].real
                    if not imag:
                        ys[k] = self[k][1][i,j].real
                    else:
                        ys[k] = self[k][1][i,j].imag
                xss.append(xs)
                yss.append(ys)
        return xss, yss

    def _get_plot_legends(self):
        leg_strs = []
        size = self._get_size()
        for i in range(size):
            for j in range(size):
                leg_strs.append(self.leg_prefix + ": "+str(i+1)+","+str(j+1))
        return leg_strs

    # Currently only supports square matrices
    def _get_size(self):
        key = random.choice(self.keys())
        return nw.shape(self[key])[0]

    def _get_reduction_container(self):
        return dVec(x_units=self.x_units, y_units=self.y_units)
