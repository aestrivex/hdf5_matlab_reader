from __future__ import division, print_function
import hdf5_matlab_reader as hmr
import numpy as np
from nose.tools import assert_raises

def test_empty_matrix():
    field = 'druzyami'
    matfile = 'samplesv73/empty_matrix.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x == hmr.EmptyMatrix()

def test_one_by_zero_empty_matrix():
    field = 'one_by_zero_empty_matrix'
    matfile = 'samplesv73/one_by_zero_empty_matrix.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x == hmr.EmptyMatrix(shape=(1, 0))

def test_two_by_zero_empty_matrix():
    field = 'two_by_zero_empty_matrix'
    matfile = 'samplesv73/two_by_zero_empty_matrix.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x == hmr.EmptyMatrix(shape=(2, 0))
