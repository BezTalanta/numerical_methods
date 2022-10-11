import math

# Ratio uses for round functions
ROUNDING_RATIO = 4

def f(x):
    return x * math.cos(x)


def test_f1(x):
    return math.log(x)


def test_f2(x):
    return math.sin(math.pi / 6 * x)


def omega(x_list):
    result = []
    for i in range(len(x_list)):
        tmp = 1
        for j in range(len(x_list)):
            if i != j:
                tmp *= x_list[i] - x_list[j]
        result.append(round(tmp, 5))
    return result


def get_multiples(x, x_list: list[float]):
    result: list[float] = []
    for i in range(len(x_list)):
        tmp = 1
        for j in range(len(x_list)):
            if j != i:
                tmp *= x - x_list[j]
        result.append(tmp)
    return result


def lagrang_get_table(x1, x2, x3, x4, first_part_letter: str):
    use_f = f
    X = [
        math.pi / 4,    # My x point
        0.8,            # First example
    ][0]                # Choose x from list above

    x_list: list[float] = [round(x1, 5), round(x2, 5), round(x3, 5), round(x4, 5)]
    f_list: list[float] = []
    omega_list: list[float] = omega(x_list)
    fdo_list: list[float] = []
    xlast_list: list[float] = []

    for idx, x in enumerate(x_list):
        f_list.append(round(use_f(x), 5))
        fdo_list.append(round(f_list[idx] / omega_list[idx], 5))
        xlast_list.append(round(X - x, 1))

    multiples_list = get_multiples(X, x_list)
    L = fdo_list[0] * multiples_list[0] + \
        fdo_list[1] * multiples_list[1] + \
        fdo_list[2] * multiples_list[2] + \
        fdo_list[3] * multiples_list[3]
    yL = use_f(X)
    precision = abs(yL - L)

    return {
        f'l{first_part_letter}_x_list': x_list,
        f'l{first_part_letter}_f_list': f_list,
        f'l{first_part_letter}_omega_list': omega_list,
        f'l{first_part_letter}_fdo_list': fdo_list,
        f'l{first_part_letter}_xlast_list': xlast_list,
        f'l{first_part_letter}_precision': round(precision, 5),
    }


def newtone_get_table(x1, x2, x3, x4, first_part_letter: str):
    use_f = f
    X = [
        math.pi / 4,    # My x point
        1.5,            # Second example
    ][0]                # Choose x from list above

    x_list: list[float] = [round(x1, 5), round(x2, 5), round(x3, 5), round(x4, 5)]
    f_list: list[float] = [round(use_f(x), 5) for x in x_list]
    fx_list: list[float] = [round((f_list[i] - f_list[i + 1])/ \
                (x_list[i] - x_list[i + 1]), 5) for i in range(3)]
    fxx_list: list[float] = [round((fx_list[0] - fx_list[1])/ \
                                   (x_list[0] - x_list[2]), 5),
                             round((fx_list[1] - fx_list[2])/ \
                                   (x_list[1] - x_list[3]), 5)]
    fxxx_list: list[float] = [round((fxx_list[0] - fxx_list[1])/ \
                                    (x_list[0] - x_list[3]), 5)]

    P = lambda x: fx_list[0]*x + fxx_list[0] * x * (x - x_list[1]) + \
            fxxx_list[0] * x * (x - x_list[1]) * (x - x_list[2])

    px = P(X)
    fx = use_f(X)

    precision = abs(fx - px)

    return {
        f'n{first_part_letter}_x_list': x_list,
        f'n{first_part_letter}_f_list': f_list,
        f'n{first_part_letter}_fx_list': fx_list,
        f'n{first_part_letter}_fxx_list': fxx_list,
        f'n{first_part_letter}_fxxx_list': fxxx_list,
        f'n{first_part_letter}_precision': round(precision, 5),
    }


def run_through_32():
    X = [
        1.5, # My variant and example
    ]

    # x_list = [0.0, 1.0, 2.0, 3.0, 4.0]              # example
    # f_list = [0.0, 1.8415, 2.9093, 3.1411, 3.2432]  # example
    x_list = [0.0, 1.0, 2.0, 3.0, 5.0]
    f_list = [0.0, 0.45345, 0.52360, 0.0, -2.2672]

    h_list = [x_list[i] - x_list[i - 1] for i in range(1, len(x_list))]

    # print('{0}c2 + {1}c3 = {2}'.format(
    #         2*(h_list[0] + h_list[1]),
    #         h_list[1],
    #         3*((f_list[2] - f_list[1])/h_list[1] - (f_list[1] - f_list[0])/h_list[0])
    #     )
    # )

    # print('{0}c2 + {1}c3 + {2}c4 = {3}'.format(
    #         h_list[1],
    #         2*(h_list[1] + h_list[2]),
    #         h_list[2],
    #         3*((f_list[3] - f_list[2])/h_list[2] - (f_list[2] - f_list[1])/h_list[1])
    #     )
    # )

    # print('{0}c3 + {1}c4 = {2}'.format(
    #         h_list[2],
    #         2*(h_list[2] + h_list[3]),
    #         3*((f_list[4] - f_list[3])/h_list[3] - (f_list[3] - f_list[2])/h_list[2]),
    #     )
    # )

    # c_list = [0.0, -0.44949, -0.52299, 0.03344] # example
    c_list = [0.0, -0.20454, -0.33174, -0.24971]

    b_list = [round((f_list[i] - f_list[i - 1])/h_list[i] -
              1/3 * h_list[i] * (c_list[i] + 2 * c_list[i - 1]), 5)
              for i in range(1, len(f_list) - 1)]
    b_list.append(round((f_list[4] - f_list[3])/h_list[3] - 2/3*h_list[3]*c_list[3], 5))
    d_list = [round((c_list[i] - c_list[i - 1])/3*h_list[i], 5)
              for i in range(1, len(f_list) - 1)]
    d_list.append(round(-c_list[3]/3*h_list[3], 5))

    end_f_func = lambda x: round(f_list[1] + b_list[1] * (x - 1) + \
            c_list[1] * ((x - 1)**2) + d_list[1] * ((x - 1)**3), 5)

    return {
        'x_list': x_list,
        'f_list': f_list,
        'b_list': b_list,
        'c_list': c_list,
        'd_list': d_list,
        'X': X[0],
        'res': end_f_func(X[0]),
    }


def run_through_33():
    # Which variant will be using, 0 - mine, 1 - example
    select_variant: int = 0

    x_list = [
        [-1, 0, 1, 2, 3, 5], # my variant
        [0, 1.7, 3.4, 5.1, 6.8, 8.5] # example
    ][select_variant]
    y_list = [
        [-0.86603, 0, 0.86603, 1, 0, -4.3301], # my variant
        [0, 1.3038, 1.8439, 2.2583, 2.6077, 2.9155] # example
    ][select_variant]

    # N + 1
    u1 = 6
    # parametr with a0 at the bottom line
    u2 = sum(x_list)
    # parametr with a1 at the upper line
    v1 = u2
    # parametr with a1 at the bottom line
    v2 = sum([round(x**2, ROUNDING_RATIO) for x in x_list])
    # parametr after equal operator at the upper line
    c1 = sum(y_list)
    # at the bottom line
    c2 = sum([round(x_list[i] * y_list[i], ROUNDING_RATIO) for i in range(len(x_list))])

    a1 = round((u1 * c2 - u2 * c1) / (u1 * v2 - u2 * v1), ROUNDING_RATIO)
    a0 = round((c1 - v1 * a1) / u1, ROUNDING_RATIO)

    F1_list = [round(a0 + a1 * x, ROUNDING_RATIO) for x in x_list]
    miss_sum1 = round(sum([(F1_list[i] - y_list[i])**2 for i in range(len(F1_list))]), ROUNDING_RATIO)

    a2: float = [
        0.3284, # my variant
        -0.0355,
    ][select_variant]
    a1: float = [
        1.0213, # my variant
        0.6193,
    ][select_variant]
    a0: float = [
        0.3284, # my variant
        0.1295,
    ][select_variant]

    F2_list = [round(a0 + a1 * x + a2 * x**2, ROUNDING_RATIO) for x in x_list]
    miss_sum2 = round(sum(
            [(F2_list[i] - y_list[i])**2 for i in range(len(F2_list))]), ROUNDING_RATIO
        )

    return {
        'x_list': x_list,
        'y_list': y_list,
        'f1_list': F1_list,
        'miss1': miss_sum1,
        'f2_list': F2_list,
        'miss2': miss_sum2,
    }
