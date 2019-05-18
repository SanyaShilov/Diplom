from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from pprint import pprint

from fuzzy_logic import *


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
pprint(rel5.composition_max_min(rel6).matrix, width=50)
pprint(rel5.composition_min_max(rel6).matrix, width=50)
pprint(rel5.composition_max_mul(rel6).matrix, width=50)

fs1 = FuzzySet(
    [
        FuzzyElement(1, 0),
        FuzzyElement(2, 0.1),
        FuzzyElement(3, 0.5),
        FuzzyElement(4, 0.8),
        FuzzyElement(5, 1),
    ]
)
fs2 = FuzzySet(
    [
        FuzzyElement(5, 1),
        FuzzyElement(10, 0.8),
        FuzzyElement(15, 0.4),
        FuzzyElement(20, 0.2),
    ]
)
rel = fs1.construct_relation(fs2)
pprint(rel.matrix)

fs3 = FuzzySet(
    [
        FuzzyElement(1, 0.3),
        FuzzyElement(2, 0.5),
        FuzzyElement(3, 1),
        FuzzyElement(4, 0.7),
        FuzzyElement(5, 0.4),
    ]
)
pprint(fs3.composition_zade(rel))
