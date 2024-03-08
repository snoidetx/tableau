import numpy as np
from main import tableau

A = np.array([[.7, .8, .9, 1, 0, 0], [.3, .2, .1, 0, 1, 0], [1, 1, -1, 0, 0, 1]])
b = np.array([[60, 20, 0]]).T
c = np.array([[-.7, .5, -.4, 0, 0, 0]]).T
tableau(A, b, c, (4, 5, 6))
