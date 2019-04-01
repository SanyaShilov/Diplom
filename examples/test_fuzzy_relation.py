from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

from const import *
from fuzzy_relation import FuzzyRelation
from fuzzy_set import FuzzyElement
from range import Range


rel1 = FuzzyRelation(
    [(x, y) for x in Range(0, 3) for y in Range(0, 3)],
    lambda el: e ** (-0.2 * (el[0] - el[1]) ** 2)
)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(*rel1.plot())
plt.show()


def f(el):
    x, y = el
    return 0 if x >= y else 1 / (1 + 5 / (x - y) ** 4)


rel2 = FuzzyRelation(
    [(x, y) for x in Range(0, 3) for y in Range(0, 3)],
    f
)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(*rel2.plot())
plt.show()

rel3 = rel1.intersection_min(rel2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(*rel3.plot())
plt.show()

rel4 = rel1.union_max(rel2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(*rel4.plot())
plt.show()

rel5 = FuzzyRelation(
    [
        FuzzyElement((1, 1), 0.1),
        FuzzyElement((1, 2), 0.2),
        FuzzyElement((2, 1), 0.8),
        FuzzyElement((2, 2), 1),
    ]
)
rel6 = FuzzyRelation(
    [
        FuzzyElement((3, 3), 0.6),
        FuzzyElement((3, 4), 0.4),
        FuzzyElement((4, 3), 0.5),
        FuzzyElement((4, 4), 0.3),
    ]
)
print(rel5.composition_max_min(rel6).matrix)
print(rel5.composition_min_max(rel6).matrix)
print(rel5.composition_max_mult(rel6).matrix)
