from __future__ import division, print_function
import hdf5_matlab_reader as hmr
import numpy as np
from nose.tools import assert_raises

def test_array2d():
    field = 'dir00'
    matfile = 'samplesv73/array2d.mat'
    x = hmr.loadmat(matfile)[field]
    print(np.sum(x), 637)
    assert np.sum(x) == 637

def test_single_string():
    field = 'gibbesh'
    matfile = 'samplesv73/single_string.mat'
    x = hmr.loadmat(matfile)[field]
    print (x, 'gibbesh')
    assert x == 'gibbesh'

def test_array3d():
    field = 'random_numbers'
    matfile = 'samplesv73/array3d.mat'
    x = hmr.loadmat(matfile)[field]
    print(np.sum(x), 124.2663)
    assert np.allclose(np.sum(x), 124.2663, atol=.001)
