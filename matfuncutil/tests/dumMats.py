import matfuncutil as mfc

def row_offset_col_gain_zeroimag(sz=100):
    d = mfc.dMat()
    _row_offset_col_gain_zeroimag(d,sz)
    return d

def row_offset_col_gain_posImag(sz=100):
    d = mfc.dMat()
    _row_offset_col_gain_posImag(d,sz)
    return d

def row_offset_col_gain_negImag(sz=100):
    d = mfc.dMat()
    _row_offset_col_gain_negImag(d,sz)
    return d

def row_offset_col_gain_posNegImag(rg=10):
    d = mfc.dMat()
    _row_offset_col_gain_posNegImag(d,rg)
    return d



def row_offset_col_gain_zeroimag_Smat(sz=100):
    d = mfc.dMat()
    _row_offset_col_gain_zeroimag(d,sz)
    return d


def _row_offset_col_gain_zeroimag(d, sz):
    for i in range(sz):
        d[float(i)] = mfc.nw.matrix([[float(i), 2*float(i)], 
                                     [10+float(i), 10+2*float(i)]])
    return d

def _row_offset_col_gain_posImag(d, sz):
    for i in range(sz):
        d[float(i)+1j] = mfc.nw.matrix([[float(i), 2*float(i)], 
                                        [10+float(i), 10+2*float(i)]])
    return d

def _row_offset_col_gain_negImag(d, sz):
    for i in range(sz):
        d[float(i)-1j] = mfc.nw.matrix([[float(i), 2*float(i)], 
                                        [10+float(i), 10+2*float(i)]])
    return d

def _row_offset_col_gain_posNegImag(d, rg):
    for i in range(-rg,rg+1):
        d[float(i)-float(i)*1j] = mfc.nw.matrix([[float(i), 2*float(i)], 
                                                [10+float(i), 10+2*float(i)]])
    return d

def _get_uni_mat():
    return mfc.nw.matrix([[pow(2.,-.5), pow(2.,-.5),0], 
                          [-pow(2.,-.5)*1.j, pow(2.,-.5)*1.j,0],
                          [0, 0,1.j]])

def _get_non_uni_mat():
    return mfc.nw.matrix([[pow(3.,-.5), pow(2.,-.5),0], 
                          [-pow(2.,-.5)*1.j, pow(3.,-.5)*1.j,0],
                          [0, 0,1.j]])

def two_unitary():
    d = mfc.dMat()
    d[1.0] = _get_uni_mat()
    d[2.0] = _get_uni_mat()
    return d

def one_unitary():
    d = mfc.dMat()
    d[1.0] = _get_uni_mat()
    d[2.0] = _get_non_uni_mat()
    return d

def none_unitary():
    d = mfc.dMat()
    d[1.0] = _get_non_uni_mat()
    d[2.0] = _get_non_uni_mat()
    return d

def get_identity():
    return mfc.nw.matrix([[1., 1.], 
                          [1., 1.]])

def _get_complex1():
    return mfc.nw.matrix([[1.+1.j, 2.+2.j], 
                          [3.+3.j, 4.+4.j]])

def get_complex1_absolute():
    return mfc.nw.matrix([[1.4142135623730950488016887242097, 2.8284271247461900976033774484194], 
                          [4.2426406871192851464050661726291, 5.6568542494923801952067548968388]])

def get_absolute_test():
    d = mfc.dMat()
    d[1.0] = get_identity()
    d[2.0] = _get_complex1()
    return d
