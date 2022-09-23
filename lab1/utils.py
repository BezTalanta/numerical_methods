import copy
import math

from config.matrix import Matrix
from config.utils import my_sign

def calculate_lu(x: Matrix, b: Matrix):
    L, U = Matrix(rows=x.rows_count, single=True), copy.deepcopy(x)
    for i in range(0, U.rows_count - 1):
        if U[i, i] == 0:
            k = i + 1
            is_swapped = False
            while k < U.rows_count:
                if U[k, i] != 0:
                    U.swap_rows(i, k)
                    L.swap_rows(i, k, only_lower_triangle=True)
                    is_swapped = True
                    break
                k += 1
            if is_swapped is not True:
                break

        for j in range(i + 1, x.cols_count):
            if U[j, i] == 0:
                continue
            L[j, i] = U.translate_matrix_by_simple_convertation(i, i, j)
    return L, U

def solve_slau_with_lu(L: Matrix, U: Matrix, b: Matrix) -> Matrix:
    z = Matrix(rows=L.rows_count, cols=1) # Lz = b
    z[0, 0] = b[0, 0]
    for i in range(1, L.rows_count):
        current_sum = 0
        for z_j in range(i):
            current_sum += L[i, z_j] * z[z_j, 0]
        z[i, 0] = b[i, 0] - current_sum

    x = Matrix(rows=U.rows_count, cols=1) # Ux = z
    if U[U.rows_count - 1, U.cols_count - 1] == 0:
        return x
    x[x.rows_count - 1, 0] = z[U.rows_count - 1, 0] / U[U.rows_count - 1, U.cols_count - 1]
    for i in range(x.rows_count - 2, -1, -1):
        current_sum = 0
        for j in range(i + 1, x.rows_count):
            current_sum += U[i, j] * x[j, 0]
        x[i, 0] = (z[i, 0] - current_sum) / U[i, i]
    return x

def calculate_pq(a: Matrix, d: Matrix):
    P, Q = Matrix(rows=a.rows_count, cols=1), \
        Matrix(rows=d.rows_count, cols=1)

    P[0, 0] = -a[0, 1] / a[0, 0]
    Q[0, 0] = d[0, 0] / a[0, 0]

    for i in range(1, a.rows_count):
        if i == a.rows_count - 1:
            P[i, 0] = 0
        else:
            P[i, 0] = -a[i, i + 1] /                  \
                (a[i, i] + a[i, i - 1] * P[i - 1, 0])
        Q[i, 0] = (d[i, 0] - a[i, i - 1] * Q[i - 1, 0]) / \
            (a[i, i] + a[i, i - 1] * P[i - 1, 0])

    return P, Q

def solve_slau_with_pq(P: Matrix, Q: Matrix):
    x = Matrix(rows=P.rows_count, cols=1)

    x[x.rows_count - 1, 0] = Q[Q.rows_count - 1, 0]
    for i in range(x.rows_count - 2, -1, -1):
        Pn = P[i, 0]
        xn = x[i + 1, 0]
        Qn = Q[i, 0]
        x[i, 0] = Pn * xn + Qn

    return x

def make_alpha_and_beta(a: Matrix, b: Matrix):
    beta: Matrix = Matrix(rows=b.rows_count, cols=1)
    alpha: Matrix = Matrix(rows=a.rows_count, cols=a.cols_count)

    for i in range(b.rows_count):
        beta[i, 0] = b[i, 0] / a[i, i]

    for row in range(a.rows_count):
        for col in range(a.cols_count):
            if row == col:
                continue
            alpha[row, col] = - a[row, col] / a[row, row]

    return alpha, beta

def iteration_process(alpha: Matrix, beta: Matrix, epsilon):
    x: list[Matrix] = [beta]
    epsilons: list[float] = []

    calculate_left_part = alpha.calculate_normal() / (1 - alpha.calculate_normal())

    current_epsilon = 1
    while current_epsilon > epsilon:
        x.append(beta + alpha * x[-1])

        current_epsilon = calculate_left_part * (x[-1] + (-x[-2])).calculate_normal()
        epsilons.append(round(current_epsilon, 4))

    return x, epsilons

def calculate_circle_matrix(a: Matrix):
    max, max_row, max_col = 0, 0, 0
    for row in range(a.rows_count):
        for col in range(a.cols_count):
            if row >= col:
                continue
            if abs(a[row, col]) > max:
                max = abs(a[row, col])
                max_row, max_col = row, col

    fi = 0
    if a[max_row, max_row] == a[max_col, max_col]:
        fi = math.pi / 4
    else:
        fi = 1/2 * math.atan(2 * max / (a[max_row, max_row] - a[max_col, max_col]))
    fi_sin, fi_cos = math.sin(fi), math.cos(fi)

    U = Matrix(rows=a.rows_count, cols=a.cols_count, single=True)
    U[max_row, max_row] = fi_cos
    U[max_row, max_col] = -fi_sin
    U[max_col, max_row] = fi_sin
    U[max_col, max_col] = fi_cos
    U.normalize_values()
    return U

def calculate_Q_R(A: Matrix):
    H_list: list[Matrix] = []
    A_list: list[Matrix] = [A]

    for i in range(A.cols_count - 1): # Pass all iterations
        v_vector: Matrix = Matrix(rows=A.rows_count, cols=1)
        for j in range(A.rows_count): # Create a vector from this iteration
            if j < i:
                v_vector[j, 0] = 0
            elif j == i:
                calc_sum = 0
                for k in range(i, A.rows_count): # Calculate sum after sign function
                    calc_sum += A_list[-1][k, i]**2
                v_vector[j, 0] = A_list[-1][i, i] + my_sign(A_list[-1][i, i], calc_sum**(0.5))
            else:
                v_vector[j, 0] = A_list[-1][j, i]

        # Calculate householder matrix
        tmp_calculation = v_vector * v_vector.get_transposed_matrix() * \
            (2 / (v_vector.get_transposed_matrix() * v_vector)[0, 0])
        H_tmp = Matrix(rows=A.rows_count, cols=A.cols_count, single=True) + (-tmp_calculation)
        H_tmp.normalize_values(2)
        H_tmp.make_values_cleaner()

        # Remember new householder matrix
        H_list.append(H_tmp)

        # Calculate A matrix
        A_tmp = H_list[-1] * A_list[-1]
        A_tmp.normalize_values(2)
        A_tmp.make_values_cleaner()

        # Change all nums to zero down from i col
        for k in range(i + 1, A.rows_count):
            A_tmp[k, i] = 0

        # Remember A matrix
        A_list.append(A_tmp)

    # Calculate Q matrix
    Q = H_list[0]
    for i in range(1, len(H_list)):
        Q *= H_list[i]

    # R matrix is last A
    return Q, A_list[-1]
