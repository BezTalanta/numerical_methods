import math

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.messages import error
from django import views

from config.utils import rowcol, generate_test
from config.matrix import Matrix
from .utils import (
    # 1
    calculate_lu,
    solve_slau_with_lu,

    # 2
    calculate_pq,
    solve_slau_with_pq,

    # 3
    make_alpha_and_beta,
    iteration_process,

    # 4
    calculate_circle_matrix,

    # 5
    calculate_Q_R,
)

class Lab11(views.View):
    def get(self, request):
        return render(request, 'lab11/lab11.html')

    def post(self, request):
        if request.POST.get('size', False) is not False:
            if request.POST['size'] == '' or int(request.POST['size']) < 1:
                return render(request, 'lab11/lab11.html', {
                    'size_error_empty': True,
                })
            request.session['size'] = request.POST['size']
            return render(request, 'enter_matrix.html', {
                **rowcol(int(request.POST['size'])),
                'b_is_required': True,
                'next_url': reverse('11'),
            })
        else:
            a_matrix = Matrix(rows=request.session['size'], **request.POST, letter='x')
            b_matrix = Matrix(rows=request.session['size'], cols=1, **request.POST, letter='b')

            L, U = calculate_lu(a_matrix, b_matrix)

            solve = solve_slau_with_lu(L, U, b_matrix)

            a_matrix.normalize_values(2, True)
            b_matrix.normalize_values(2, True)
            L.normalize_values(2, True)
            U.normalize_values(2, True)
            solve.normalize_values(2, True)
            det = round(a_matrix.get_determinant(), 2)
            inv = a_matrix.get_inversed_matrix()
            inv.normalize_values(2, True)

            return render(request, 'lab11/result.html', {
                'matrix_a': a_matrix,
                'matrix_ab': b_matrix,
                'matrix_l': L,
                'matrix_u': U,
                'matrix_x': solve,
                'det': det,
                'inv': inv,
            })


class Lab12(views.View):
    '''
        Pn = -cn/bn, Qn = dn/bn
    '''
    def get(self, request):
        return render(request, 'lab12/lab12.html')

    def post(self, request):
        if request.POST.get('size', False) is not False:
            if int(request.POST['size']) < 1:
                return redirect(reverse('12'))
            request.session['size'] = request.POST['size']
            return render(request, 'enter_matrix.html', {
                **rowcol(int(request.POST['size'])),
                'b_is_required': True,
                'next_url': reverse('12'),
            })
        else:
            a_matrix = Matrix(rows=request.session['size'], **request.POST, letter='x')
            d_matrix = Matrix(rows=request.session['size'], cols=1, **request.POST, letter='b')

            P, Q = calculate_pq(a_matrix, d_matrix)

            x = solve_slau_with_pq(P, Q)

            x.normalize_values(2, True)
            P.normalize_values(2, True)
            Q.normalize_values(2, True)

            return render(request, 'lab12/result.html', {
                'matrix_a': a_matrix,
                'matrix_ab': d_matrix,
                'matrix_p': P,
                'matrix_q': Q,
                'matrix_x': x,
            })


class Lab13(views.View):
    def get(self, request):
        return render(request, 'lab13/lab13.html')

    def post(self, request):
        if request.POST.get('size', False) is not False:
            if request.POST['size'] == '':
                return render(request, 'lab13/lab13.html', {
                    'size_error_empty': True,
                    'saved_precision': request.POST['precision'],
                })
            if request.POST['precision'] == '':
                return render(request, 'lab13/lab13.html', {
                    'saved_size': request.POST['size'],
                    'precision_error_empty': True,
                })
            if int(request.POST['size']) < 1:
                return redirect(reverse('13'))
            request.session['size'] = request.POST['size']
            request.session['precision'] = request.POST['precision']

            return render(request, 'enter_matrix.html', {
                **rowcol(int(request.POST['size'])),

                # Tests, have to be deleted
                # **(generate_test(10, 1, 1, 2, 10, 1, 2, 2, 10, rows=3, cols=3).to_html('x')),
                # **(generate_test(12, 13, 14, rows=3, cols=1).to_html('b')),
                #

                'b_is_required': True,
                'next_url': reverse('13'),
            })
        else:
            a = Matrix(rows=request.session['size'], letter='x', **request.POST)
            b = Matrix(rows=request.session['size'], cols=1, letter='b', **request.POST)
            eps = float(request.session['precision'])

            alpha, beta = make_alpha_and_beta(a, b)

            alpha.normalize_values(2, True)
            beta.normalize_values(2, True)

            x, epss = iteration_process(alpha, beta, eps)

            return render(request, 'lab13/result.html', {
                'matrix_a': a,
                'matrix_ab': b,
                'matrix_alpha': alpha,
                'matrix_beta': beta,
                'list_of_matrix_x': x,
                'epsilons': epss,
            })

class Lab14(views.View):
    def get(self, request):
        return render(request, 'lab14/lab14.html')

    def post(self, request):
        if request.POST.get('size', False) is not False:
            if request.POST['size'] == '':
                return render(request, 'lab14/lab14.html', {
                    'size_error_empty': True,
                    'saved_precision': request.POST['precision'],
                })
            if request.POST['precision'] == '':
                return render(request, 'lab14/lab14.html', {
                    'saved_size': request.POST['size'],
                    'precision_error_empty': True,
                })
            if int(request.POST['size']) < 1:
                return redirect(reverse('14'))

            request.session['size'] = request.POST['size']
            request.session['precision'] = request.POST['precision']

            return render(request, 'enter_matrix.html', {
                **rowcol(int(request.POST['size'])),
                'next_url': reverse('14'),

                # Example
                **(generate_test(4, 2, 1, 2, 5, 3, 1, 3, 6, rows=3, cols=3).to_html('x')),
                #
            })
        else:
            a = Matrix(rows=request.session['size'], letter='x', **request.POST)

            U_list: list[Matrix] = []
            A_list: list[Matrix] = [a]

            original_epsilon = float(request.session['precision'])
            t_list = []
            t_tmp = original_epsilon + 0.1

            extra_exit = 0
            while t_tmp > original_epsilon:
                U_list.append(calculate_circle_matrix(A_list[-1]))

                A_tmp = U_list[-1].get_transposed_matrix() * A_list[-1] * U_list[-1]
                A_tmp.normalize_values()

                A_list.append(A_tmp)

                t_tmp = 0
                for row in range(A_tmp.rows_count - 1):
                    for col in range(row + 1, A_tmp.cols_count):
                        t_tmp += A_tmp[row, col]**2
                t_tmp **= 0.5

                t_list.append(t_tmp)

                extra_exit += 1
                if extra_exit == 50:
                    return render(request, 'lab14/t_out.html', {
                        'list_t': t_list,
                    })

            list_lambda = []
            for row in range(A_list[-1].rows_count):
                list_lambda.append(A_list[-1][row, row])

            big_u = U_list[0]
            for u in U_list[1:]:
                big_u *= u

            own_vectors = []
            for i in range(big_u.cols_count):
                matrix_tmp = Matrix(rows=big_u.rows_count, cols=1)
                for j in range(big_u.rows_count):
                    matrix_tmp[j, 0] = big_u[j, i]
                own_vectors.append(matrix_tmp)

            U_list.append(None)

            return render(request, 'lab14/result.html', {
                'matrix_a': a,
                'list_U': U_list,
                'list_A': A_list,
                'list_lambda': list_lambda,
                'own_vectors': own_vectors,
            })


class Lab15(views.View):
    def get(self, request):
        return render(request, 'lab15/lab15.html')

    def post(self, request):
        if request.POST.get('size', False) is not False:
            if request.POST['size'] == '':
                return render(request, 'lab15/lab15.html', {
                    'size_error_empty': True,
                    'saved_precision': request.POST['precision'],
                })
            if request.POST['precision'] == '':
                return render(request, 'lab15/lab15.html', {
                    'saved_size': request.POST['size'],
                    'precision_error_empty': True,
                })
            if int(request.POST['size']) < 1:
                return redirect(reverse('15'))

            request.session['size'] = request.POST['size']
            request.session['precision'] = request.POST['precision']

            return render(request, 'enter_matrix.html', {
                **rowcol(int(request.POST['size'])),
                'next_url': reverse('15'),

                # Example
                # **(generate_test(1, 3, 1, 1, 1, 4, 4, 3, 1, rows=3, cols=3).to_html('x')),
                #
            })
        else:
            a = Matrix(rows=request.session['size'], letter='x', **request.POST)
            eps = float(request.session['precision'])

            extra_exit_count = 0
            t_list = []
            A_list = [a]
            Q_list = []
            R_list = []
            while extra_exit_count < 50:
                Q, R = calculate_Q_R(A_list[-1])

                Q_list.append(Q)
                R_list.append(R)

                tmp = R * Q
                tmp.normalize_values(4)
                tmp.make_values_cleaner()
                A_list.append(tmp)

                end = False
                for i in range(A_list[-1].cols_count - 1):
                    current_sum = 0
                    for j in range(i + 1, A_list[-1].rows_count):
                        current_sum += A_list[-1][j, i]**2
                    t_list.append(current_sum**(0.5))
                    if current_sum**(0.5) <= eps:
                        end = True
                        break

                if end is True:
                    break

                extra_exit_count += 1

            if extra_exit_count == 50:
                return render(request, 'lab15/t_out.html', {
                    'list_t': t_list,
                })

            lambda_matrix = Matrix(rows=a.rows_count, cols=1)
            if a.rows_count < 3:
                for i in range(lambda_matrix.rows_count):
                    lambda_matrix[i, i] = A_list[-1][i, i]
            else:
                for i in range(lambda_matrix.rows_count - 1):
                    lambda_matrix[i, 0] = A_list[-1][i, i]
                    if i == lambda_matrix.rows_count - 2:
                        x1, x2 = A_list[-1][i, i], A_list[-1][i, i + 1]
                        y1, y2 = A_list[-1][i + 1, i], A_list[-1][i + 1, i + 1]
                        deskriminant = (x1 + x2)**2 - 4 * (x1 * y2 - x2 * y1)
                        lambda_matrix[i, 0] = (x1 + y2 + deskriminant**(0.5)) / 2
                        lambda_matrix[i, 0] = round(lambda_matrix[i, 0].real, 2) \
                            + round(lambda_matrix[i, 0].imag, 2) * 1j
                        lambda_matrix[i + 1, 0] = (x1 + y2 - deskriminant**(0.5)) / 2
                        lambda_matrix[i + 1, 0] = \
                            round(lambda_matrix[i + 1, 0].real, 2) + \
                            round(lambda_matrix[i + 1, 0].imag, 2) * 1j

            return render(request, 'lab15/result.html', {
                'matrix_a': a,
                'list_A': A_list,
                'lambdas': lambda_matrix,
            })
