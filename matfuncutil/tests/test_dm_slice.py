import os
import sys
basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,basedir+'/../..')

import pynumwrap as nw
import dumMats

import unittest

class test_int_element_access(unittest.TestCase):
    def runTest(self):
        d1 = dumMats.row_offset_col_gain_posNegImag()
        self.assertEqual(len(d1),21)
        sorted_keys = d1.sorted_keys()
        sortedVal = d1.sorted_values()
        for i in range(21):
            kv = d1[i]
            self.assertEqual(kv[0], sorted_keys[i])
            nw.are_matrices_close(kv[1], sortedVal[i])


class slice_test_helper(unittest.TestCase):
    def cal_pos_neg_imag_ene(self, i):
        return float(i)-float(i)*1j
    def cal_pos_neg_imag_sub_mat(self, i):
        return nw.matrix([[float(i), 2*float(i)], 
                         [10+float(i), 10+2*float(i)]])
    def check_pos_neg_imag_sub(self, d, sortedVal, i, i_off, val):
        actKey = float(i_off)-float(i_off)*1j
        actMat = self.cal_pos_neg_imag_sub_mat(i_off)
        self.assertEqual(val,actKey)
        nw.are_matrices_close(sortedVal[i],actMat)
        nw.are_matrices_close(d[val],actMat)

class test_complex_element_access(slice_test_helper):
    def runTest(self):
        d1 = dumMats.row_offset_col_gain_posNegImag()
        sorted_keys = d1.sorted_keys()
        sortedVal = d1.sorted_values()
        for i,val in enumerate(sorted_keys):
            i_off = i-10
            self.check_pos_neg_imag_sub(d1, sortedVal, i, i_off, val)

class test_simp_slice(slice_test_helper):
    def runTest(self):
        d1 = dumMats.row_offset_col_gain_posNegImag()
        d2 = d1[1:-1]
        self.assertEqual(len(d2),19)
        sorted_keys = d2.sorted_keys()
        sortedVal = d2.sorted_values()
        for i,val in enumerate(sorted_keys):
            i_off = i-9
            self.check_pos_neg_imag_sub(d1, sortedVal, i, i_off, val)

class test_step_slice(slice_test_helper):
    def runTest(self):
        d1 = dumMats.row_offset_col_gain_posNegImag()
        d2 = d1[::2]
        self.assertEqual(len(d2),11)
        sorted_keys = d2.sorted_keys()
        sortedVal = d2.sorted_values()
        for i,val in enumerate(sorted_keys):
            i_off = i*2-10
            self.check_pos_neg_imag_sub(d1, sortedVal, i, i_off, val)

class test_step_sliceRange(slice_test_helper):
    def runTest(self):
        d1 = dumMats.row_offset_col_gain_posNegImag()
        d2 = d1[1:-1:2]
        self.assertEqual(len(d2),10)
        sorted_keys = d2.sorted_keys()
        sortedVal = d2.sorted_values()
        for i,val in enumerate(sorted_keys):
            i_off = i*2-9
            self.check_pos_neg_imag_sub(d1, sortedVal, i, i_off, val)
        
class test_get_slice_indices(slice_test_helper):
    def runTest(self):
        d1 = dumMats.row_offset_col_gain_posNegImag()

        ret = d1.get_slice_indices(0,20,3)
        self.assertEqual(ret[0],(0,21,10))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-10),
                                 self.cal_pos_neg_imag_ene(10)))

        ret = d1.get_slice_indices(1,19,3)
        self.assertEqual(ret[0],(1,20,9))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-9),
                                 self.cal_pos_neg_imag_ene(9)))

        ret = d1.get_slice_indices(0,20,4)
        self.assertEqual(ret[0],(0,19,6))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-10),
                                 self.cal_pos_neg_imag_ene(8)))

        ret = d1.get_slice_indices(1,19,4)
        self.assertEqual(ret[0],(1,20,6))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-9),
                                 self.cal_pos_neg_imag_ene(9)))

        ret = d1.get_slice_indices(0,20,10)
        self.assertEqual(ret[0],(0,19,2))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-10),
                                 self.cal_pos_neg_imag_ene(8)))

        ret = d1.get_slice_indices(1,19,10)
        self.assertEqual(ret[0],(1,20,2))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-9),
                                 self.cal_pos_neg_imag_ene(9)))

        ret = d1.get_slice_indices(2,19,10)
        self.assertEqual(ret[0],(2,12,1))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-8),
                                 self.cal_pos_neg_imag_ene(1)))
        
class test_calculate_reduction_indices_from_end(slice_test_helper):
    def runTest(self):
        d1 = dumMats.row_offset_col_gain_posNegImag()

        ret = d1.get_slice_indices(0,20,3,True)
        self.assertEqual(ret[0],(0,21,10))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-10),
                                 self.cal_pos_neg_imag_ene(10)))

        ret = d1.get_slice_indices(1,19,3,True)
        self.assertEqual(ret[0],(1,20,9))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-9),
                                 self.cal_pos_neg_imag_ene(9)))

        ret = d1.get_slice_indices(0,20,4,True)
        self.assertEqual(ret[0],(2,21,6))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-8),
                                 self.cal_pos_neg_imag_ene(10)))

        ret = d1.get_slice_indices(1,19,4,True)
        self.assertEqual(ret[0],(1,20,6))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-9),
                                 self.cal_pos_neg_imag_ene(9)))

        ret = d1.get_slice_indices(0,20,10,True)
        self.assertEqual(ret[0],(2,21,2))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-8),
                                 self.cal_pos_neg_imag_ene(10)))

        ret = d1.get_slice_indices(1,19,10,True)
        self.assertEqual(ret[0],(1,20,2))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(-9),
                                 self.cal_pos_neg_imag_ene(9)))

        ret = d1.get_slice_indices(2,19,10,True)
        self.assertEqual(ret[0],(10,20,1))
        self.assertEqual(ret[1],(self.cal_pos_neg_imag_ene(0),
                                 self.cal_pos_neg_imag_ene(9)))


if __name__ == "__main__":
    #Just for debug
    b = test_step_slice()
    b.runTest()
