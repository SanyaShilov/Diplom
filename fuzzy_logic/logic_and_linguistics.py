from utils.range import Range


BOOL_RANGE = Range(0, 1)


def unary_operation(o):
    def modified(f):
        def result(x):
            return o(f, x)
        return result
    return modified


def binary_operation(o):
    def modified(f1, f2):
        def result(x):
            return o(f1, f2, x)
        return result
    return modified


@unary_operation
def f_not(f, x):
    return 1 - f(x)


@unary_operation
def f_very(f, x):
    return f(x) ** 2


@unary_operation
def f_more_or_less(f, x):
    return f(x) ** 0.5


@binary_operation
def f_and(f1, f2, x):
    return min(f1(x), f2(x))


@binary_operation
def f_or(f1, f2, x):
    return max(f1(x), f2(x))


@binary_operation
def f_imp(f1, f2, x):
    return max(1 - f1(x), f2(x))


def truth_zade(x, a=0.4):
    return (
        0 if x <= a else
        2 * ((x - a) / (1 - a)) ** 2 if x <= (a + 1) / 2 else
        1 - 2 * ((1 - x) / (1 - a)) ** 2
    )


def lie_zade(x, a=0.4):
    return truth_zade(1 - x, a)


def truth_baldwin(x):
    return x


def lie_baldwin(x):
    return 1 - x


def clear_truth(x):
    return 1 if x == 1 else 0


def clear_lie(x):
    return 1 if x == 0 else 0


__all__ = [
    'BOOL_RANGE',
    'f_not', 'f_very', 'f_more_or_less',
    'f_and', 'f_or', 'f_imp',
    'truth_zade', 'lie_zade',
    'truth_baldwin', 'lie_baldwin',
    'clear_truth', 'clear_lie',
]
