# tableau

The Tableau Method provides a convenient way to solve linear programming (LP) problems. This repository provides a Python implementation of the Tableau method.

## Usage

1. Before using, make sure the LP problem is in the **standard form** (e.g., by adding slack variables if necessary), that is
```math
\begin{matrix} \min & \mathbf{c}^\top \mathbf{x} \\ \mathrm{s.t.} & \mathbf{A}\mathbf{x} = \mathbf{b} \\ & \mathbf{x} \geq \mathbf{0}. \end{matrix}
```

2. Input $\mathbf{A}$, $\mathbf{b}$, $\mathbf{c}$ and the column numbers of starting bases with to ```calculate.py``` file.
3. Run ```python3 calculate.py```.

## Example

### Input in ```calculate.py```

```
import numpy as np
from main import tableau

A = np.array([[.7, .8, .9, 1, 0, 0], [.3, .2, .1, 0, 1, 0], [1, 1, -1, 0, 0, 1]])
b = np.array([[60, 20, 0]]).T
c = np.array([[-.7, .5, -.4, 0, 0, 0]]).T
tableau(A, b, c, (4, 5, 6))
```

### Output

```
min -0.7x1 + -0.5x2 + -0.4x3 + 0.0x4 + 0.0x5 + 0.0x6 
s.t. Ax = b, x >= 0, where 
A = 
[[ 0.7  0.8  0.9  1.   0.   0. ]
 [ 0.3  0.2  0.1  0.   1.   0. ]
 [ 1.   1.  -1.   0.   0.   1. ]],
b = 
[[60]
 [20]
 [ 0]].
==========
Initial tableau:
Basic     x1        x2        x3        x4        x5        x6        Solution  
c         -0.7      -0.5      -0.4      0.0       0.0       0.0       
reduced c -0.7      -0.5      -0.4      0         0         0         0.0       
x4        0.7       0.8       0.9       1.0       0.0       0.0       60.0      
x5        0.3       0.2       0.1       0.0       1.0       0.0       20.0      
x6        1.0       1.0       -1.0      0.0       0.0       1.0       0.0       

Possible entering variables: [1, 2, 3]
Please choose an entering variable:
```

Here you should select one of the variables from $x_1$, $x_2$ or $x_3$ as the **entering variable**, and repeat this process until an optimal solution is found or the problem is found to be unbounded:

```
Please choose an entering variable: 2
== Iteration 1 ==
Basic     x1        x2        x3        x4        x5        x6        Solution  
c         -0.7      -0.5      -0.4      0.0       0.0       0.0       
reduced c -0.2      0.0       -0.9      0.0       0.0       0.5       0.0       
x4        -0.1      0.0       1.7       1.0       0.0       -0.8      60.0      
x5        0.1       0.0       0.3       0.0       1.0       -0.2      20.0      
x2        1.0       1.0       -1.0      0.0       0.0       1.0       0.0       

Possible entering variables: [1, 3]
Please choose an entering variable: 1
== Iteration 2 ==
Basic     x1        x2        x3        x4        x5        x6        Solution  
c         -0.7      -0.5      -0.4      0.0       0.0       0.0       
reduced c 0.0       0.2       -1.1      0.0       0.0       0.7       0.0       
x4        0.0       0.1       1.6       1.0       0.0       -0.7      60.0      
x5        0.0       -0.1      0.4       0.0       1.0       -0.3      20.0      
x1        1.0       1.0       -1.0      0.0       0.0       1.0       0.0       

Possible entering variables: [3]
Please choose an entering variable: 3
== Iteration 3 ==
Basic     x1        x2        x3        x4        x5        x6        Solution  
c         -0.7      -0.5      -0.4      0.0       0.0       0.0       
reduced c 0.0       0.2688    0.0       0.6875    0.0       0.2188    41.25     
x3        0.0       0.0625    1.0       0.625     0.0       -0.4375   37.5      
x5        0.0       -0.125    0.0       -0.25     1.0       -0.125    5.0       
x1        1.0       1.0625    0.0       0.625     0.0       0.5625    37.5      

All reduced costs >= 0. END.
```
