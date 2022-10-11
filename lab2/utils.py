import math

from config.matrix import Matrix
from config.utils import generate_test


def test1_f(x):
    return math.exp(2*x) + 3 * x - 4


def test1_df(x):
    return 2 * math.exp(2 * x) + 3


def f(x):
    return math.log10(2*x + 1) - x**3 + 1


def df(x):
    # ddf: (-4 * ln(10))/(2*ln(10)*x+1)^2 - 6x
    return 2 / (math.log(10) * (2 * x + 1)) - 3 * x**2

'''
                       3
    f = log  (2x+1) - x + 1
           10
                                    1/3                     1/3
    phi(x) = (log  (2x+1) + log  10)    = (log  (2x+1) * 10)
                 10            10             10
'''
def phi(x):
    return math.pow(math.log10((2*x+1)*10), 1/3)


def dphi(x):
    return (2 * math.pow(10, 1/3)) / \
        (math.pow(math.log(10), 1/3) * (6 * x + 3) * math.pow(math.log(2*x+1), 2/3))


def simple_newtone_method(eps):
    x_list = [float(0.6)]
    f_list = []
    df_list = []
    mf_list = []

    count = 0
    while count == 0 or abs(x_list[-1] - x_list[-2]) >= float(eps):
        xk = x_list[-1]
        f_list.append(round(f(xk), 4))
        df_list.append(round(df(xk), 4))
        mf_list.append(round(-f_list[-1]/df_list[-1], 4))

        x_list.append(round(xk - f_list[-1]/df_list[-1], 4))

        count += 1

    return {
        'newtone_x_list': x_list,
        'newtone_f_list': f_list,
        'newtone_df_list': df_list,
        'newtone_mf_list': mf_list,
    }


def simple_iterations(eps):
    q = abs(dphi(0.6))
    q_part = q/(1-q)

    x_list = [0.3]
    phi_list = [round(phi(0.3), 4)]

    status = float(eps) + 1
    while status > float(eps):
        x_list.append(round(phi_list[-1], 4))
        phi_list.append(round(phi(x_list[-1]), 4))

        status = q_part * abs(x_list[-1] - x_list[-2])

    return {
        'iter_x_list': x_list,
        'iter_phi_list': phi_list,
    }

'''
     x1x2
    e     + x1 - 4 = 0
      2
    x1  - 4x2 - 1 = 0

    1.5 < x1(x) < 2
    0.5 < x2(y) < 1.0

    phi1:
        y: phi1 = ln(4/x - 1)
    phi2:
        x: phi2 = +- sqrt(4*y + 1)
'''
def hf1(x, y):
    return math.exp(x*y) + x - 4

# def hf1(x, y):
#     return 0.1 * x**2 + x + 0.2 * y**2 - 0.3

def hdxf1(x, y):
    return y * math.exp(x*y) + 1

# def hdxf1(x, y):
#     return 0.2 * x + 1

def hdyf1(x, y):
    return x * math.exp(x*y)

# def hdyf1(x, y):
#     return 0.4 * y

'''
      2
    x1  - 4x2 - 1 = 0

'''
def hf2(x, y):
    return x**2 - 4*y - 1

# def hf2(x, y):
#     return 0.2 * x**2 + y - 0.1 * x * y - 0.7

def hdxf2(x, y):
    return 2*x

# def hdxf2(x, y):
#     return 0.4 * x - 0.1 * y

def hdyf2(x, y):
    return -4

# def hdyf2(x, y):
#     return 1 - 0.4 * x
''''''

def hard_newtone_method(eps):
    x_list: list[list[float]] = [
            [1.75, 0.75]
            # [0.25, 0.75]
        ]
    f_list: list[list[float]] = []
    dfx_list: list[list[float]] = []
    dfy_list: list[list[float]] = []
    deta1_list: list[float] = []
    deta2_list: list[float] = []
    detj_list: list[float] = []

    status = float(eps) + 1
    while status > float(eps):
        x1k, x2k = x_list[-1][0], x_list[-1][1]

        f_list.append([round(hf1(x1k, x2k), 5), round(hf2(x1k, x2k), 5)])
        dfx_list.append([round(hdxf1(x1k, x2k), 5), round(hdxf2(x1k, x2k), 5)])
        dfy_list.append([round(hdyf1(x1k, x2k), 5), round(hdyf2(x1k, x2k), 5)])

        A1 = generate_test(f_list[-1][0], dfy_list[-1][0],
                           f_list[-1][1], dfy_list[-1][1], rows=2, cols=2)

        A2 = generate_test(dfx_list[-1][0], f_list[-1][0],
                           dfx_list[-1][1], f_list[-1][1], rows=2, cols=2)

        J = generate_test(dfx_list[-1][0], dfy_list[-1][0],
                          dfx_list[-1][1], dfy_list[-1][1], rows=2, cols=2)

        # print(J)

        deta1_list.append(A1.get_determinant())
        deta2_list.append(A2.get_determinant())
        detj_list.append(J.get_determinant())

        x_list.append(
                [round(x1k - deta1_list[-1]/detj_list[-1], 5),
                    round(x2k - deta2_list[-1]/detj_list[-1], 5)]
            )

        status = max(x_list[-1][0] - x1k, x_list[-1][1] - x2k)

    # print(x_list)

    return {
        'newtone_x_list': x_list,
        'newtone_f_list': f_list,
        'newtone_dfx_list': dfx_list,
        'newtone_dfy_list': dfy_list,
        'newtone_deta1_list': deta1_list,
        'newtone_deta2_list': deta2_list,
        'newtone_detj_list': detj_list,
    }

# def hphi1(x, y):
#     return 0.3 - 0.1 * x**2 - 0.2 * y**2

# def hdxphi1(x, y):
#     return 0.7 - 0.2 * x**2 + 0.1 * x * y

# def hdxphi1(x, y):
#     return -0.2 * x

# def hdyphi1(x, y):
#     return -0.4 * y

# def hphi2(x, y):
#     return 0.7 - 0.2 * x**2 + 0.1 * x * y

# def hdxphi2(x, y):
#     return -0.4 * x + 0.1 * y

# def hdyphi2(x):
#     return 0.1 * x

'''
    phi1:
        y: phi1 = ln(4/x - 1)
    phi2:
        x: phi2 = +- sqrt(4*y + 1)

'''
def hphi1(x, y):
    return 4 - math.exp(x * y)
    # return math.log(4/x - 1)

def hdxphi1(x, y):
    return -y * math.exp(x * y)

def hdyphi1(x, y):
    return -x * math.exp(x * y)

def hphi2(x, y):
    return (x**2 - 1) / 4
    # return math.sqrt(4*y + 1)

def hdxphi2(x, y):
    return x / 2

def hdyphi2():
    return 0

def hard_iteration_method(eps):
    # q_part = 1 # 0.75 / 0.25

    x_list: list[list[float]] = [
            [1.75, 0.75]
            # [0.25, 0.75]  # example
        ]
    phi_list: list[list[float]] = []

    status = float(eps) + 1
    counter = 0
    while status > float(eps):
        counter += 1
        phi_tmp: list[float] = [hphi1(x_list[-1][0], x_list[-1][1]),
                                hphi2(x_list[-1][0], x_list[-1][1])]
        phi_list.append(phi_tmp)
        x_list.append(phi_tmp)
        if counter == 5:
            break
        print(counter, phi_tmp)

        status = max(abs(x_list[-1][0] - x_list[-2][0]),
                            abs(x_list[-1][1] - x_list[-2][1]))

    return {
        'iter_x_list': x_list,
        'iter_phi_list': phi_list,
    }
