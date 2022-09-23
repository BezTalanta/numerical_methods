import copy
import math

class Matrix:
    rows_count, cols_count = 0, 0
    data: list[list[int]] = []

    def __init__(self, **kwargs):
        '''
            **kwargs:
                Required:
                    1. rows: defines how many rows your matrix will have,
                        if cols is not define, matrix will be square matrix with size: rows * rows
                    2. a lot of x<number><number> or b<number><number> and it required letter
                        letter: defines what system will take from data,
                            'x' will take x<number><number> or 'b' will take b<number>
                            if it didn't be sent, system won't check to x or b

                If you wish:
                    cols: defines how many cols your matrix will have, use it for rectangle matrix
                    single: defines if your matrix will have '1' on a diagonal line
                    matrix: make a copy from other matrix
        '''
        self.data = []
        if kwargs.get('rows', False) is not False:
            rows = int(kwargs['rows'])
            self.rows_count = rows
        else:
            raise ValueError("You hadn't send rows")
        cols = int(kwargs['cols']) if kwargs.get('cols', False) is not False else rows
        self.cols_count = cols
        single = True if kwargs.get('single', False) is not False else False

        for i in range(rows):
            tmp = []
            for j in range(cols):
                if i == j and single is True:
                    tmp.append(1)
                else:
                    tmp.append(0)
            self.data.append(tmp)

        letter = kwargs['letter'] if kwargs.get('letter', False) is not False else False
        if letter is not False:
            for key, value in kwargs.items():
                if letter == 'x':
                    x_index = key.find('x')
                    if x_index == -1:
                        continue

                    if type(value) is not list:
                        self.data[int(key[0:x_index])][int(key[x_index + 1:])] = value
                    else:
                        self.data[int(key[0:x_index])][int(key[x_index + 1:])] = int(value[0])
                elif letter == 'b' and key[0] == 'b':
                    if type(value) is not list:
                        self.data[int(key[1:])][0] = value
                    else:
                        self.data[int(key[1:])][0] = int(value[0])

    def fill_from_other_matrix(self, matrix):
        if self.rows_count != matrix.rows_count or \
            self.cols_count != matrix.cols_count:
            raise ValueError('Your matrices have a different size')
        self.data = copy.deepcopy(matrix.data)

    def get_triangle_count(self):
        return (self.cols_count * self.cols_count - self.cols_count) / 2

    def swap_rows(self, first_row, second_row, **kwargs):
        if kwargs.get('only_lower_triangle', False) is not False:
            for i in range(self.cols_count):
                if i == first_row:
                    return
                self.data[first_row][i], self.data[second_row][i] = \
                    self.data[second_row][i], self.data[first_row][i]
        self.data[first_row], self.data[second_row] = \
            self.data[second_row], self.data[first_row]

    def translate_matrix_by_simple_convertation(self, row, col, second_row):
        ratio = self.data[second_row][col] / self.data[row][col]
        self.data[second_row][col] = 0
        for i in range(col + 1, self.cols_count):
            self.data[second_row][i] -= self.data[row][i] * ratio
        return ratio

    def normalize_values(self, digits=4, make_cleaner=False):
        for row in range(self.rows_count):
            for col in range(self.cols_count):
                self.data[row][col] = round(self.data[row][col], digits)
                # self.data[row][col] = math.ceil(self.data[row][col])
        if make_cleaner:
            self.make_values_cleaner()

    def make_values_cleaner(self):
        '''
            Clears all -0.0 or -4.0 and something like that
        '''
        for row in range(self.rows_count):
            for col in range(self.cols_count):
                current_value = self[row, col]
                if float(current_value) == int(current_value):
                    self[row, col] = int(current_value)

    def calculate_normal(self, euklid=False):
        if self.cols_count == 1:
            result = 0
            if not euklid:
                for i in range(self.rows_count):
                    if i == 0 or abs(self[i, 0]) > result:
                        result = abs(self[i, 0])
                return round(result, 4)
            else:
                for i in range(self.rows_count):
                    result += abs(self[i, 0])**2
                return result**(0.5)
        normal = 0.0
        for i in range(self.cols_count):
            tmp_result = 0
            for j in range(self.rows_count):
                tmp_result += abs(self[j, i])
            if i == 0 or tmp_result > normal:
                normal = tmp_result
        return round(normal, 4)

    def to_html(self, letter='x'):
        result_map = {}
        for i in range(self.rows_count):
            for j in range(self.cols_count):
                result_map[f'{i}{letter}{j}'] = self[i, j]
        return result_map

    def change_diagonal_to_non_zero(self) -> bool:
        for i in range(self.rows_count):
            if self[i, i] == 0:
                passed = False
                for k in range(i + 1, self.rows_count):
                    if self[k, i] != 0:
                        passed = True
                        self.swap_rows(i, k)
                        break
                if not passed:
                    return False
        return True

    def get_cols(self):
        return range(self.cols_count)

    def get_rows(self):
        return range(self.rows_count)

    def get_transposed_matrix(self):
        new_matrix = Matrix(rows=self.cols_count, cols=self.rows_count)
        for row in range(self.rows_count):
            for col in range(self.cols_count):
                new_matrix[col, row] = self[row, col]
        return new_matrix

    def get_determinant(self, digits=5):
        if self.rows_count != self.cols_count:
            raise Exception('Your matrix is not square matrix')
        cursed_matrix = copy.deepcopy(self)
        status = cursed_matrix.change_diagonal_to_non_zero()
        if status is False:
            return 0
        for i in range(cursed_matrix.rows_count - 1):
            if cursed_matrix[i, i] == 0:
                return 0
            for j in range(i + 1, cursed_matrix.rows_count):
                cursed_matrix.translate_matrix_by_simple_convertation(i, i, j)
        determinant = cursed_matrix[0, 0]
        for i in range(1, cursed_matrix.rows_count):
            determinant *= cursed_matrix[i, i]
        return round(determinant, digits)

    def get_inversed_matrix(self):
        full_matrix = Matrix(rows=self.rows_count, cols=self.cols_count * 2, letter='x', **self.to_html('x'))
        status = full_matrix.change_diagonal_to_non_zero()
        if status is False:
            raise Exception('Your matrix cannot be inversed')

        determinant = self.get_determinant()
        if determinant == 0:
            raise Exception("Determinant equal 0, so inversed matrix isn't exist")

        # Fill '1' to right single matrix
        for rowcol in range(full_matrix.rows_count):
            full_matrix[rowcol, rowcol + self.cols_count] = 1

        # Forward algorithm
        for row in range(full_matrix.rows_count):
            # Check only lower triangle
            for k in range(row + 1, full_matrix.rows_count):
                full_matrix.translate_matrix_by_simple_convertation(row, row, k)

        # Backward algorithm
        for row in range(full_matrix.rows_count - 1, 0, -1):
            # Check only upper triangle
            for k in range(row - 1, -1, -1):
                full_matrix.translate_matrix_by_simple_convertation(row, row, k)

        for row in range(full_matrix.rows_count):
            if full_matrix[row, row] != 1:
                rem = full_matrix[row, row]
                for k in range(full_matrix.cols_count):
                    full_matrix[row, k] /= rem

        inversed_matrix = Matrix(rows=self.rows_count, cols=self.cols_count)
        for row in range(self.rows_count):
            for col in range(self.cols_count):
                inversed_matrix[row, col] = full_matrix[row, col + self.cols_count]
        inversed_matrix.make_values_cleaner()
        return inversed_matrix

    def __getitem__(self, row_col):
        row, col = row_col
        if row < 0 or col < 0:
            raise ValueError('Your row or col less than 0')
        if row >= len(self.data) or col >= len(self.data[0]):
            raise ValueError("Your row or col more than matrix size, \
remember matrix's index starts with 0")
        return self.data[row][col]

    def __setitem__(self, row_col, new_value):
        row, col = row_col
        if row < 0 or col < 0:
            raise IndexError('Your row or col less than 0')
        if row >= len(self.data) or col >= len(self.data[0]):
            raise IndexError("Your row or col more than matrix size, \
remember matrix's index starts with 0")
        self.data[row][col] = new_value

    def __add__(self, variable):
        if self.rows_count != variable.rows_count or \
            self.cols_count != variable.cols_count:
            raise Exception('Your matrices have a different size')
        return_m = Matrix(rows=self.rows_count, cols=self.cols_count)
        for row in range(self.rows_count):
            for col in range(self.cols_count):
                return_m[row, col] = self.data[row][col] + \
                    variable[row, col]
        return_m.normalize_values()
        return return_m

    def __neg__(self):
        return_m = Matrix(rows=self.rows_count, cols=self.cols_count)
        for row in range(self.rows_count):
            for col in range(self.cols_count):
                return_m[row, col] = -self[row, col]
        return return_m

    def __mul__(self, variable):
        if type(variable) == Matrix:
            if self.cols_count != variable.rows_count:
                raise Exception('Your matrices have a wrong size')
            return_m = Matrix(rows=self.rows_count, \
                        cols=variable.cols_count)
            for i in range(self.rows_count):
                for j in range(variable.cols_count):
                    tmp_result = 0
                    for k in range(variable.rows_count):
                        tmp_result += self[i, k] * variable[k, j]
                    return_m[i, j] = tmp_result
            return_m.normalize_values()
            return return_m
        else:
            matrix_return = Matrix(rows=self.rows_count, cols=self.cols_count)
            for i in range(self.rows_count):
                for j in range(self.cols_count):
                    matrix_return[i, j] = self[i, j] * variable
            return matrix_return

    def __str__(self) -> str:
        return_str = '-' * 10 + 'Matrix output' + '-' * 10 + '\n'
        for row in self.data:
            return_str += '\t' + str(row) + '\n'
        return_str += '-' * 8 + 'Matrix output end' + '-' * 8 + '\n'
        return return_str