# coding=utf-8

import matplotlib.pyplot as pt
import numpy as np
from scipy.optimize import leastsq
from pylab import *

time = []
counts = []
for i in open('/some/folder/to/file.txt', 'r'):
    segs = i.split()
    time.append(float(segs[0]))
    counts.append(segs[1])
time_array = arange(len(time), dtype=float)
counts_array = arange(len(counts))
time_array[0:] = time
counts_array[0:] = counts


def model(time_array0, coeffs0):
    a = coeffs0[0] + coeffs0[1] * np.exp(- ((time_array0 - coeffs0[2]) / coeffs0[3]) ** 2)
    b = coeffs0[4] + coeffs0[5] * np.exp(- ((time_array0 - coeffs0[6]) / coeffs0[7]) ** 2)
    c = a + b
    return c


def residuals(coeffs, counts_array, time_array):
    return counts_array - model(time_array, coeffs)


# 0 = baseline, 1 = amplitude, 2 = centre, 3 = width
peak1 = np.array([0, 6337, 16.2, 4.47, 0, 2300, 13.5, 2], dtype=float)
# peak2 = np.array([0,2300,13.5,2], dtype=float)
x, flag = leastsq(residuals, peak1, args=(counts_array, time_array))
# z, flag = leastsq(residuals, peak2, args=(counts_array, time_array))
plt.plot(time_array, counts_array)
plt.plot(time_array, model(time_array, x), color='g')
# plt.plot(time_array, model(time_array, z), color = 'r')
plt.show()
