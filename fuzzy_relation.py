import collections
import numpy as np

from fuzzy_set import FuzzySet, FuzzyElement


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
        self.z = np.array([
            [self[i * self.ylen + j].p for j in range(self.ylen)]
            for i in range(self.xlen)
        ])

    def plot(self):
        return self.x, self.y, self.z

    # TODO: refactor compositions to remove code duplication

    def composition_max_min(self, other: 'FuzzyRelation'):
        return FuzzyRelation(
            [
                FuzzyElement(
                    (self.x[i][0], other.y[0][j]),
                    max(
                        min(self.z[i][k], other.z[k][j]) for k in range(self.ylen)
                    )
                )
                for j in range(other.ylen)
                for i in range(self.xlen)
            ]
        )

    def composition_min_max(self, other: 'FuzzyRelation'):
        return FuzzyRelation(
            [
                FuzzyElement(
                    (self.x[i][0], other.y[0][j]),
                    min(
                        max(self.z[i][k], other.z[k][j]) for k in range(self.ylen)
                    )
                )
                for j in range(other.ylen)
                for i in range(self.xlen)
            ]
        )

    def composition_max_mult(self, other: 'FuzzyRelation'):
        return FuzzyRelation(
            [
                FuzzyElement(
                    (self.x[i][0], other.y[0][j]),
                    max(
                        self.z[i][k] * other.z[k][j] for k in range(self.ylen)
                    )
                )
                for j in range(other.ylen)
                for i in range(self.xlen)
            ]
        )
