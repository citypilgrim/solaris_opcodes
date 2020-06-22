import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


Dcoeff_a = [
    1.007364e+00, -5.961937e-05, 7.952000e-08, -3.058268e-11, 6.313052e-15,
    -7.574798e-19, 5.529103e-23, -2.484367e-27, 6.703068e-32, -9.953326e-37,
    6.249791e-42
]

def D_f(n_ara):
    '''
    input of n_ara should be MHz, corrected to kHz in the function
    '''
    corr_ara = np.sum([
        Dcoeff * ((n_ara*1e3)**i) for i, Dcoeff in enumerate(Dcoeff_a)
    ], axis=0)
    return corr_ara

a = np.array([15.32091]*4)
a = a[1:2]
print(a.dtype)
print(D_f(a))
