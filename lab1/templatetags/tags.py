import random

from django import template

from config.matrix import Matrix

register = template.Library()

# @register.simple_tag(takes_context=True)
# def gen_m(context, letter, html_name, letter_b=None):
#     matrix: Matrix = context[f'matrix_{letter}']
#     matrix_b: Matrix = context[f'matrix_{letter_b}'] \
#         if letter_b is not None else None
#     result_string: list[str] = []
#     for row in range(matrix.rows_count):
#         if row == matrix.rows_count / 2:
#             result_string.append(html_name + '    ')
#         else:
#             result_string.append('\t')
#         for col in range(matrix.cols_count):
#             if col == 0:
#                 result_string[-1] += str(matrix[row, col])
#                 # result_string += str(matrix[row, col])
#             else:
#                 result_string[-1] += ' + ' + str(matrix[row, col])
#                 # result_string += ' + ' + str(matrix[row, col])

#         if letter_b is not None:
#             result_string[-1] += ' = ' + str(matrix_b[row, 0])

#     return result_string

@register.simple_tag(takes_context=True)
def get_value(context, name_of_matrix, row, col):
    if context.get(name_of_matrix, False) is False:
        raise Exception(f"Your context hasn't {str(name_of_matrix)}, check context")
    return context[name_of_matrix][row, col]

@register.simple_tag
def get_value_from_list(in_list, index):
    return in_list[index]

@register.simple_tag(takes_context=True)
def get_rows(context, matrix_name):
    if context.get(matrix_name, False) is False:
        raise Exception(f"{matrix_name} doesn't exist in the context")
    return range(context[matrix_name].rows_count)

@register.simple_tag(takes_context=True)
def get_cols(context, matrix_name):
    if context.get(matrix_name, False) is False:
        raise Exception(f"{matrix_name} doesn't exist in the context")
    return range(context[matrix_name].cols_count)

@register.simple_tag(takes_context=True)
def fill_matrix(context, row, letter, col):
    key = f'{row}{letter}{col}'
    if context.get(key, False) is not False:
        return context[key]
    return random.randint(1, 10)

@register.simple_tag(takes_context=True)
def debug_print(context):
    print(context)
