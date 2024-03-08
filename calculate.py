from main import tableau
import numpy as np


AA = np.array([[1, 1, 1, -1]])
bb = np.array([[3]]).T
cc = np.array([[- 1, -1, -1, -1]]).T
tableau(AA, bb, cc, (1,))
