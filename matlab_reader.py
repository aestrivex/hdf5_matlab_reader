import sys
import h5py
import numpy as np
from functools import partial

def extract_file(f):
    return {k:extract_element(f, v) for k, v in f.iteritems()}

def extract_element(f, element):
    if type(element) == h5py._hl.dataset.Dataset:
        return extract_dataset(f, element)
    elif type(element) == h5py._hl.group.Group:
        return extract_group(f, element)
    else:
        raise NotImplementedError('Unimplemented HDF5 structure')

def extract_group(f, group):
    #remove slash delimiters from group names
    return {k:extract_element(f, v) for k, v in group.iteritems()}

def extract_dataset(f, dataset):
    print dir(dataset)

    if dataset.dtype == np.float64:
        #double
        return dataset.value

    elif dataset.dtype == np.dtype:
        #cell
        return extract_cell(f, dataset)

    elif dataset.dtype == np.uint16:
        #string
        return extract_string(dataset)

def extract_cell(f, dataset):
    '''
    behold the elegance and simplicity of recursion
    '''
    return map_ndarray(
        partial(extract_dataset, f),
        np.array(map(
                    partial(map_ndarray, lambda y:f[y]),
                    dataset.value)))

def extract_string(dataset):
    #return map_ndarray(chr, dataset.value)
    #map_ndarray( reduce( lambda x,y:chr(x)+chr(y), dataset.value) )
    
    #return map_ndarray( reduce( lambda x,y:chr(x)+chr(y), np.array(dataset) ))

    string_k = partial(map_ndarrays, lambda z: ''.join(map(chr, z)))

#                    lambda z: reduce( lambda x,y:chr(x)+chr(y),
 #                                     map( int, z ) ))

    #string_k = partial(map_ndarrays, 
    #                partial(reduce, lambda x,y:chr(x)+chr(y)))

    #string_k = partial(map_ndarray, 
    #    lambda z:reduce( 
    #                lambda x,y:chr(x)+chr(y), 
    #                z))
    
    #import pdb
    #pdb.set_trace()
    return string_k(dataset.value)

    #return partial(map_ndarrays, lambda z: ''.join(map(chr, z)))(dataset.value)


def map_ndarray( k, ndarray ):
    '''
    like map, but operates on every element of n-dimensional np.ndarray
    '''
    if ndarray.ndim > 1:
        #return np.array(map( partial(map_ndarray, callable), ndarray ))
        return map( partial(map_ndarray, k), ndarray )
    else:
        #return np.array(map( callable, ndarray ))
        return map( k, ndarray )

def map_ndarrays( k, ndarray ):
    '''
    like map, but operates on every lowest-dim list of n-dimensional np.ndarray
    '''
    if ndarray.ndim > 1:
        #return np.array(map( partial(map_ndarray, callable), ndarray ))
        return map( partial(map_ndarrays, k), ndarray )
    else:
        #return np.array(map( callable, ndarray ))
        return k( ndarray )


if __name__ == '__main__':
    matfile = sys.argv[1]

    h5_file = h5py.File(matfile, 'r')

    mat_out = extract_file(h5_file)    

    #print mat_out

    for k, v in mat_out.iteritems():
        print k, np.shape(v)

