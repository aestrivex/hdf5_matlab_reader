from __future__ import division, print_function
import hdf5_matlab_reader as hmr
import numpy as np
from nose.tools import assert_raises

def test_sparse_array():
    field = 'few_numbers'
    matfile = 'samplesv73/sparse_array.mat'
    x = hmr.loadmat(matfile)[field]
    print(repr(x))
    print(x)
    assert tuple(x.shape) == (100, 100)
    assert x.max() == 98
    assert x.sum() == 185

def test_sparse_asym():
    field = 'sparse_asym'
    matfile = 'samplesv73/sparse_asym.mat'
    x = hmr.loadmat(matfile)[field]
    print(repr(x))
    print(x)
    assert tuple(x.shape) == (30, 40)
    assert x.max() == 55
    assert x.sum() == 63 
    
def test_sparse_transchiral():
    field = 'sparse_transchiral'
    matfile = 'samplesv73/sparse_transchiral.mat'
    x = hmr.loadmat(matfile)[field]
    print(repr(x))
    print(x)
    assert tuple(x.shape) == (40, 30)
    assert x.max() == 44
    assert x.sum() == 51
