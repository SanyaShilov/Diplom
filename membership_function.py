from const import *


def triangular(a, b, c):
    assert a < b < c

    def f(x):
        return (
            0 if x < a else
            (x - a) / (b - a) if x < b else
            1 - (x - b) / (c - b) if x < c else
            0
        )
    return f


def trapezoidal(a, b, c, d):
    assert a < b <= c < d

    def f(x):
        return (
            0 if x < a else
            (x - a) / (b - a) if x < b else
            1 if x < c else
            1 - (x - c) / (d - c) if x < d else
            0
        )
    return f


def gaussian(b, c):
    def f(x):
        return e ** -((x - b) ** 2 / (2 * c ** 2))
    return f


def sigmoid(a, c):
    def f(x):
        return 1 / (1 + e ** -(a * (x - c)))
    return f


def singleton(a):
    def f(x):
        return 1 if abs(x - a) < EPS else 0
    return f
