__author__ = 'yxu01'
import numpy as np
def randoom_exchange (array,labelarr,iter):
    def swap_rows(arr, frm, to):
        if arr.shape == (arr.shape[0],):# a vector
            arr[[frm, to]] = arr[[to, frm]]
        else : #a matrix
            arr[[frm, to],:] = arr[[to, frm],:]

    for i in range(iter):
        b = np.random.randint(0,array.shape[0],2)
        swap_rows(array,b[0],b[1])
        swap_rows(labelarr,b[0],b[1])



