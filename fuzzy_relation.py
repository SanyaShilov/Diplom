import collections
import numpy as np
import operator

from fuzzy_element import FuzzyElement
from fuzzy_set import FuzzySet


def composition(summation, multiplication):
    def func(self: 'FuzzyRelation', other: 'FuzzyRelation'):
        return FuzzyRelation(
            [
                FuzzyElement(
                    (self.x[i][0], other.y[0][j]),
                    summation(
                        multiplication(self.z[i][k], other.z[k][j])
                        for k in range(self.ylen)
                    )
                )
                for j in range(other.ylen)
                for i in range(self.xlen)
            ]
        )
    return func


class FuzzyRelation(FuzzySet):
    def __init__(self, elements, f=None):
        super().__init__(elements, f)
        counter = collections.Counter((element.x[0] for element in self))
        self.xlen = len(counter)
        self.ylen = len(self) // self.xlen if self.xlen else 0
        self.matrix = [
            [self[i * self.ylen + j] for j in range(self.ylen)]
            for i in range(self.xlen)
        ]
        self.x = [
            [self[i * self.ylen + j].x[0] for j in range(self.ylen)]
            for i in range(self.xlen)
        ]
        self.y = [
            [self[i * self.ylen + j].x[1] for j in range(self.ylen)]
            for i in range(self.xlen)
        ]
        self.z = [
            [self[i * self.ylen + j].p for j in range(self.ylen)]
            for i in range(self.xlen)
        ]

    def plot(self):
        return self.x, self.y, np.array(self.z)

    def as_set(self):
        return FuzzySet(
            (FuzzyElement(el.x[1], el.p) for el in self),
            lambda x: self.f((0, x)) if self.f else None
        )

    composition_max_min = composition(max, min)
    composition_min_max = composition(min, max)
    composition_max_mul = composition(max, operator.mul)
