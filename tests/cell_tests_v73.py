from __future__ import division, print_function
import hdf5_matlab_reader as hmr
import numpy as np
from nose.tools import assert_raises

def test_empty_cell():
    field = 'tschik'
    matfile = 'samplesv73/empty_cell.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x == hmr.EmptyMatrix()

def test_cells_integers():
    field = 'goomer'
    matfile = 'samplesv73/cells_integers.mat'
    x = hmr.loadmat(matfile)[field]
    print(x, np.sum(x), 280)
    assert np.sum(x) == 280

def test_cells_strings():
    field = 'words'
    matfile = 'samplesv73/cells_strings.mat'
    x = hmr.loadmat(matfile)[field]
    print(x, 'tulk hamik safoj')
    assert tuple(x) == ('tulk', 'hamik', 'safoj')

def test_many_empty_cells():
    field = 'manycells'
    matfile = 'samplesv73/many_empty_cells.mat'
    x = hmr.loadmat(matfile)[field]
    print(np.shape(x), '138x6')
    assert np.prod(np.shape(x)) == 828

def test_cell_with_one_by_zero_empty_matrix():
    field = 'cell_with_one_by_zero_empty_matrix'
    matfile = 'samplesv73/cell_with_one_by_zero_empty_matrix.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x == hmr.EmptyMatrix(shape=(1, 0))

def test_cell_with_two_by_zero_empty_matrix():
    field = 'cell_with_two_by_zero_empty_matrix'
    matfile = 'samplesv73/cell_with_two_by_zero_empty_matrix.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x == hmr.EmptyMatrix(shape=(2, 0))

def test_some_cells():
    field = 'somecells'
    matfile = 'samplesv73/some_cells.mat'
    x = hmr.loadmat(matfile)[field]
    print(x, 34)
    assert np.sum(x) == 34

def test_nested_cells():
    field = 'nest_cells'
    matfile = 'samplesv73/nested_cells.mat'
    x = hmr.loadmat(matfile)[field]
    empty = hmr.EmptyMatrix()
    empty_nest = np.array([empty, empty, np.array([empty, empty])])
    print(x, empty_nest)
    assert x.sum().sum(dtype=int) == 0
    for xi, ei in zip(x, empty_nest):
        assert np.all(xi == ei)

def test_complex_cells():
    field = 'complex_cells'
    matfile = 'samplesv73/complex_cells.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert len(x) == 4
    assert_raises(ValueError, np.sum, x)
    assert x[0][0] + x[2][1] == 15
