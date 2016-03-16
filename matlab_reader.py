#!/usr/bin/env python

import sys
import h5py
import numpy as np
from functools import partial

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
    #print dir(dataset)

    print 'korent', dataset, type(dataset)

    if type(dataset) is not h5py._hl.dataset.Dataset:
        #for extracting a cell. depending on the cell type, cells can have
        #child datasets that cast to human readable data types, such as
        #datasets of floats can cast directly to np.ndarray, so nothing needed
        return dataset

    elif dataset.dtype.str in ('<f8', '<f4'):
        #float64, float32
        return dataset.value

    elif dataset.dtype.str in ('|O8',):
        #object, that is, dtype == np.dtype
        #matlab cell/cellarray
        return extract_cell(f, dataset)

    elif dataset.dtype.str in ('<u2',):
        #string (uint16)
        return extract_string(dataset)

    elif dataset.dtype.str in ('<u8',):
        #empty cell (uint64)
        return None

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

def bytearray_to_string(z):
    return ''.join(map(chr, z))

def extract_string(dataset):
    string_k = partial(map_ndarrays, bytearray_to_string)
    #char arrays are transposed in matlab representation
    #column and row are opposite, but not in terms of order on disk
    return string_k(np.transpose(dataset.value))


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

def is_ndim_list(ndlist):
    return list in map(type, ndlist)

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

    h5_file = h5py.File(matfile, 'r')
    
    try:
        mat_out = extract_file(h5_file)    

        print mat_out

        for k, v in mat_out.iteritems():
            print k, np.shape(v)

        import pdb
        pdb.set_trace()
    except Exception as e:
        print '{0}: {1}'.format(type(e), e)
        import pdb
        pdb.set_trace()
