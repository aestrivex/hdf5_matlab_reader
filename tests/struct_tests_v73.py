from __future__ import division, print_function
import hdf5_matlab_reader as hmr
import numpy as np
from nose.tools import assert_raises

def test_empty_struct():
    field = 'empty_struct'
    matfile = 'samplesv73/empty_struct.mat'
    x = hmr.loadmat(matfile)[field]
    print(x, 'empty dict')
    assert x == {}

def test_basic_struct():
    field = 'basic_struct'
    matfile = 'samplesv73/basic_struct.mat'
    record1 = 'fish'
    record2 = 'donkey'
    record3 = 'toenail'
    x = hmr.loadmat(matfile)[field]
    print(x[record1], 23)
    assert x[record1] == 23
    print(x[record2], 'donkey')
    assert x[record2] == 'donkey'
    print(x[record3], '[31, 55]')
    assert np.sum(x[record3]) == 86 

def test_char_array_struct():
    field = 'smallstruct'
    matfile = 'samplesv73/char_array_struct.mat'
    record = 'ch_names'
    x = hmr.loadmat(matfile)[field]
    print('len(x)', len(x[record]), 307)
    assert len(x[record]) == 307 
    print('x[4]', x[record][4], 'MEG 0123')
    assert x[record][4] == 'MEG 0123'
    ch_name_lens = map(len, x[record])
    assert np.all(np.array(ch_name_lens) == 8)
