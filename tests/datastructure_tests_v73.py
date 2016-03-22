from __future__ import division, print_function
import hdf5_matlab_reader as hmr
import numpy as np
from nose.tools import assert_raises

def test_categorical_array():
    matfile = 'samplesv73/categorical_array.mat'
    x = hmr.loadmat(matfile)
    print(x['#subsystem#']['MCOS'])
    assert 'RI' in x['#subsystem#']['MCOS'][2]

def test_datetime_object():
    #dont even know what to do with this stupid number
    #its essentially some kind of currenttimeinmillis index
    #lets just make sure it loads properly
    field = 'times'
    matfile = 'samplesv73/datetime_object.mat'
    x = hmr.loadmat(matfile)
    assert field in x

def test_map_object():
    pass

def test_table_object():
    pass
