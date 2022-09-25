import math


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
