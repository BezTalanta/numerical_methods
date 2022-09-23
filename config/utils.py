from .matrix import Matrix

def rowcol(rows: int, cols: int = None):
    if cols is None:
        cols = rows
    return {'cols': range(cols), 'rows': range(rows)}

def generate_test(*args, **kwargs):
    rows = None if kwargs.get('rows', False) is False else kwargs['rows']
    cols = None if kwargs.get('cols', False) is False else kwargs['cols']
    if rows is None or cols is None:
        raise Exception('You have to send rows and cols count to generate test')
    if len(args) != rows * cols:
        raise Exception(f'Your args len is {len(args)} but you sent this \
{rows * cols} size')

    result: Matrix = Matrix(rows=rows, cols=cols)
    for idx, arg in enumerate(args):
        result[idx // cols, idx % cols] = arg
    return result

def my_sign(argument_of_sign, attach_sign_to_this_variable):
    if argument_of_sign >= 0:
        return attach_sign_to_this_variable
    return -attach_sign_to_this_variable
