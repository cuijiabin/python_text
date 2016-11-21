# coding=gbk

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def simData():
    dt = 0.0001
    d1 = 0.25
    d2 = 0.25
    v1 = 12
    v2 = 5
    while True:
        d1 += v1 * dt
        d2 += v2 * dt
        if (d1 > 1) or (d1 < 0):
            v1 = -v1
        if (d2 > 1) or (d2 < 0):
            v2 = -v2
        yield d1, d2


def simPoints(simData):
    d1, d2 = simData[0], simData[1]
    line.set_data(d1, d2)
    return line


fig = plt.figure()
ax = fig.add_subplot(111)
line, = ax.plot([], [], 'bo', ms=10)
ax.set_ylim(0, 1)
ax.set_xlim(0, 1)
ani = animation.FuncAnimation(fig, simPoints, simData, blit=False, interval=1, repeat=True)
plt.show()