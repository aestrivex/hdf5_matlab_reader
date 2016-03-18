#!/usr/bin/env python

import sys
import h5py
import numpy as np
from functools import partial
from empty_matrix import EmptyMatrix

def loadmat(f):
    h5_file = h5py.File(f, 'r')
    return extract_file(h5_file)

def extract_file(f):
    def avoid_refs(kv):
        k, v = kv
        #return True
        return not k.startswith(u'#refs#')

    return {k:extract_element(f, v) for k, v in filter(avoid_refs,
                                                       f.iteritems())}

def extract_element(f, element):
    if type(element) is h5py._hl.dataset.Dataset:
        return extract_dataset(f, element)
    elif type(element) is h5py._hl.group.Group:
        return extract_group(f, element)
    else:
        raise NotImplementedError('Unimplemented HDF5 structure')

def extract_group(f, group):
    return {k:extract_element(f, v) for k, v in group.iteritems()}

def extract_dataset(f, dataset):
    data_class = dataset.attrs['MATLAB_class']
    
    #print 'korent', dataset, type(dataset)

    if data_class == 'struct' and 'MATLAB_empty' in dataset.attrs:
        #check immediately for empty struct
        return {}

    elif 'MATLAB_empty' in dataset.attrs and dataset.attrs['MATLAB_empty'] == 1:
        #empty matrix if shape in 0xN, Nx0
        #size of empty matrix encoded as its value. several strategies possible
        #1. Ignore size of empty matrix, return None. Probably acceptable
        #2. Return np.empty(shape=shape). Causes odd behavior if the
        #   shape is actually desired, for instance 138x6 cell array of empty
        #   matrices (0 by 0) returns as 138x6x0x0 np.ndarray
        #3. Return placeholder empty matrix class which correctly conveys
        #   matrix size

        #type of empty can be numerical, or canonical_empty
        return EmptyMatrix(shape=dataset.value, dtype=data_class)

    elif data_class in ('double', 'single', 'int8', 'uint8', 'int16', 'uint16',
                      'int32', 'uint32', 'int64', 'uint64'):
        #numerical arrays
        return dataset.value

    elif data_class == 'logical':
        #encoded in matlab as ubyte, we force as bool
        return dataset.value.astype(bool)

    elif data_class in ('cell', 'FileWrapper__'):
        return extract_cell(f, dataset)

    elif data_class == 'char':
        return extract_string(dataset)

    elif data_class in ('categorical',):
        return dataset.value

def indexarg(f, arg):
    '''
    clearly it is more important to be pythonic than straightforward
    '''
    return f[arg]

def extract_cell(f, dataset):
    '''
    behold the elegance and simplicity of recursion
    '''
    return np.squeeze(
            map_ndlist(
             partial(extract_dataset, f),
             map(partial(map_ndarray,
                         partial(indexarg, f)),
                 dataset.value)))

def byte_to_unicode(b):
    return str(b).decode('hex').decode('utf-8')

def bytearray_to_string(z):
    return ''.join(map(unichr, z))

def is_ndim_list(ndlist):
    return list in map(type, ndlist)

def extract_string(dataset):
    string_k = partial(map_ndarrays, bytearray_to_string)
    #char arrays are transposed in matlab representation
    #column and row are opposite, but not in terms of order on disk
    str_array = string_k(np.transpose(dataset.value))

    #if the result is a single string, return just the single string
    #otherwise, return the full character array
    if len(str_array) == 1:
        return str_array[0]
    else:
        return str_array

def map_ndlist(k, ndlist):
    '''
    like map, but operates on every element of n-dimensional python list
    '''
    if type(ndlist) == list:
        return map(partial(map_ndlist, k), ndlist)
    else:
        return k(ndlist)

def map_ndarray(k, ndarray):
    '''
    like map, but operates on every element of n-dimensional np.ndarray
    '''
    if ndarray.ndim > 1:
        return map(partial(map_ndarray, k), ndarray)
    else:
        return map(k, ndarray)

def map_ndlists(k, ndlists):
    '''
    like map, but operates on every lowest-dim list of n-dimensional list
    '''
    if is_ndim_list(ndlists):
        return map(partial(map_ndlist, k), ndlist)
    else:
        return k(ndlist)

def map_ndarrays(k, ndarray):
    '''
    like map, but operates on every lowest-dim list of n-dimensional np.ndarray
    '''
    if ndarray.ndim > 1:
        return map(partial(map_ndarrays, k), ndarray)
    else:
        return k(ndarray)


if __name__ == '__main__':
    matfile = sys.argv[1]

    try:
        h5_file = h5py.File(matfile, 'r')
        mat_out = extract_file(h5_file)

        print mat_out

        for k, v in mat_out.iteritems():
            print k, np.shape(v)

        import pdb
        pdb.set_trace()
    except Exception as e:
        print('{0}: {1}'.format(type(e), e))
        import pdb
        pdb.set_trace()
