import math


def distance(p1, p2):
    return lv(vector(p1, p2))


def vector(p1, p2):
    return p2[0] - p1[0], p2[1] - p1[1]


def lv(v):
    return (v[0] ** 2 + v[1] ** 2) ** 0.5


def scalar_p(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def p_plus_v(p, v):
    return p[0] + v[0], p[1] + v[1]


def degree_v(v1, v2):
    lv1 = lv(v1)
    lv2 = lv(v2)
    if lv1 and lv2:
        return math.acos(scalar_p(v1, v2) / lv(v1) / lv(v2)) * 180 / math.pi
    return 0


def degree_p(p1, p2, p3):
    return degree_v(vector(p1, p2), vector(p1, p3))


__all__ = [
    'distance', 'vector', 'lv', 'scalar_p', 'p_plus_v', 'degree_v', 'degree_p'
]
