#vim: set fileencoding=UTF-8 :

from __future__ import division, print_function
import hdf5_matlab_reader as hmr
import numpy as np
from nose.tools import assert_raises

def test_data_types():
    field = 'data_types'
    matfile = 'samplesv73/data_types.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x['byte'].dtype == np.int8
    assert x['ubyte'].dtype == np.uint8
    assert x['short'].dtype == np.int16
    assert x['ushort'].dtype == np.uint16
    assert x['int'].dtype == np.int32
    assert x['uint'].dtype == np.uint32
    assert x['long'].dtype == np.int64
    assert x['ulong'].dtype == np.uint64
    assert x['single'].dtype == np.float32
    assert x['double'].dtype == np.float64
    assert x['bool'].dtype == np.bool

def test_function_handle():
    field = 'funhandle'
    matfile = 'samplesv73/function_handle.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    # X is a weird struct with information about the function handle
    # we really dont care what it is we just care that it shows something about
    # whats in the file and that it is a function handle
    assert 'function_handle' in x
    
def test_cyrillic_string():
    field = 'zelonij'
    matfile = 'samplesv73/cyrillic_string.mat'
    x = hmr.loadmat(matfile)[field]
    print(x)
    assert x == u'зелёный'
