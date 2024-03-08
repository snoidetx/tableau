import numpy as np
import copy


def nrows(A):
    return A.shape[0]


def ncols(A):
    return A.shape[1]


def equal_width(s, width=10):
    s_new = ""
    if len(s) < 10:
        s_new = s + ' ' * (10 - len(s))
    return s_new


def bfs(A, b, base_indices):
    base_indices_zero = tuple(i - 1 for i in base_indices)
    A_B = A[:, base_indices_zero]
    x_B = np.matmul(np.linalg.inv(A_B), b)
    return x_B


def _ensemble_tableau(n_iter, c, rcs, rows, entering_set):
    nvars = nrows(c)
    first_row = f"== Iteration {n_iter} ==\n"
    first_row += equal_width("Basic")
    for i in range(nvars):
        first_row += equal_width(f"x{i + 1}")
    first_row += equal_width("Solution")

    second_row = equal_width("c")
    for i in range(nvars):
        second_row += equal_width(f"{np.round(c[i, 0], decimals=4)}")

    third_row = equal_width("reduced c")
    for i in range(nvars):
        rc = rcs[i]
        rc = np.round(rc, decimals=4)
        third_row += equal_width(f"{rc}")

    third_row += equal_width(f"{np.round(rcs[-1], decimals=4)}")

    remaining_rows = ""
    for i in range(len(entering_set)):
        remaining_rows += equal_width(f"x{entering_set[i] + 1}")
        for j in range(nvars + 1):
            remaining_rows += equal_width(f"{np.round(rows[i][j], decimals=4)}")
        remaining_rows += '\n'

    return first_row + '\n' + second_row + '\n' + third_row + '\n' + remaining_rows


def tableau(A, b, c, base_indices):
    prob_statement = r"min "
    for i in range(nrows(c)):
        prob_statement += str(c[i, 0]) + f"x{i + 1} + "
    prob_statement = prob_statement[0:-2]
    prob_statement += '\n'
    prob_statement += f"s.t. Ax = b, x >= 0, where \nA = \n{str(A)},\nb = \n{str(b)}."
    print(prob_statement)

    first_row = "==========\nInitial tableau:\n"
    first_row += equal_width("Basic")
    for i in range(nrows(c)):
        first_row += equal_width(f"x{i + 1}")
    first_row += equal_width("Solution")

    second_row = equal_width("c")
    for i in range(nrows(c)):
        second_row += equal_width(f"{c[i, 0]}")

    A_B = A[:, tuple(i - 1 for i in base_indices)]
    c_B = c[tuple(i - 1 for i in base_indices), :]
    third_row = equal_width("reduced c")
    rcs = np.zeros(nrows(c) + 1)
    for i in range(nrows(c)):
        rc = 0
        if i + 1 in base_indices:
            rc = 0
        else:
            c_j = c[i, 0]
            A_j = A[:, (i,)]
            rc = c_j - (np.transpose(c_B) @ np.linalg.inv(A_B) @ A_j)[0, 0]
            rc = np.round(rc, decimals=4)
        rcs[i] = rc
        third_row += equal_width(f"{rc}")

    obj = (-np.transpose(c_B) @ bfs(A, b, base_indices))[0, 0]
    obj = np.round(obj, decimals=4)
    rcs[-1] = obj
    third_row += equal_width(f"{obj}")

    entering_set = [i - 1 for i in base_indices]
    nvars = ncols(A)
    ndim = ncols(A_B)
    rows = np.zeros((ndim, nvars + 1))
    for i in range(len(entering_set)):
        for j in range(nvars):
            if j not in entering_set:
                A_j = A[:, (j,)]
                rows[i][j] = (np.linalg.inv(A_B) @ A_j)[i, 0]
            elif j == entering_set[i]:
                rows[i][j] = 1
        rows[i][-1] = bfs(A, b, base_indices)[i, 0]

    remaining_rows = ""
    for i in range(len(entering_set)):
        remaining_rows += equal_width(f"x{entering_set[i] + 1}")
        for j in range(nvars + 1):
            remaining_rows += equal_width(f"{np.round(rows[i][j], decimals=4)}")
        remaining_rows += '\n'

    print(first_row)
    print(second_row)
    print(third_row)
    print(remaining_rows)

    n_iter = 0

    while True:
        if np.all(rcs[:-1] >= 0):
            print("All reduced costs >= 0. END.")
            break

        n_iter += 1

        entering_vars = []
        for i in range(nvars):
            if rcs[i] < 0:
                entering_vars.append(i)

        print("Possible entering variables: " + str([i + 1 for i in entering_vars]))
        entering_var = int(input("Please choose an entering variable: ")) - 1

        min_dist = 999999
        leaving_var_index = None
        for i in range(len(entering_set)):
            dist = rows[i][-1] / rows[i][entering_var]
            if rows[i][entering_var] <= 0:
                continue
            if dist < min_dist:
                leaving_var_index = i
                min_dist = dist

        if leaving_var_index == None:
            print("Problem is unbounded. END.")
            return

        entering_set[leaving_var_index] = entering_var
        normalizer = rows[leaving_var_index][entering_var]
        rows[leaving_var_index] /= normalizer

        for i in range(len(entering_set)):
            if i != leaving_var_index:
                normalizer = rows[i][entering_var]
                rows[i] = rows[i] - normalizer * rows[leaving_var_index]

        normalizer = rcs[entering_var]
        rcs = rcs - normalizer * rows[leaving_var_index]

        print(_ensemble_tableau(n_iter, c, rcs, rows, entering_set))
