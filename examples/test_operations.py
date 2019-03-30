from matplotlib import pyplot as plt

from fuzzy_set import FuzzySet
from range import Range


def plot_unary_operation(fs, operation, subplot=None, show=False):
    result = getattr(fs, operation)()
    target = plt
    if subplot:
        target = plt.subplot(*subplot)
    target.plot(list(fs.values()), list(fs.probabilities()))
    target.plot(list(result.values()), list(result.probabilities()))
    plt.grid(True)
    if show:
        plt.show()


def plot_binary_operation(fs1, fs2, operation, subplot=None, show=False):
    result = getattr(fs1, operation)(fs2)
    target = plt
    if subplot:
        target = plt.subplot(*subplot)
    target.plot(list(fs1.values()), list(fs1.probabilities()))
    target.plot(list(fs2.values()), list(fs2.probabilities()))
    target.plot(list(result.values()), list(result.probabilities()))
    plt.grid(True)
    if show:
        plt.show()


fs = FuzzySet(Range(7, 16), lambda x: 0.6 / (1 + (10 - x) ** 2))
plot_unary_operation(fs, 'normalized', show=True)


fs = FuzzySet(Range(0, 10), lambda x: x / 4 - 0.5 if 2 <= x <= 6 else 4 - x / 2 if 6 <= x <= 8 else 0)
plot_unary_operation(fs, 'complement', show=True)


r = Range(0, 10)
fs1 = FuzzySet(r, lambda x: 1 / (1 + (5 - x) ** 2))
fs2 = FuzzySet(r, lambda x: max(x if x <= 1 else 1 + 1/9 - x / 9, 0))

plot_binary_operation(fs1, fs2, 'intersection_min', (2, 3, 1))
plot_binary_operation(fs1, fs2, 'intersection_mult', (2, 3, 2))
plot_binary_operation(fs1, fs2, 'intersection_lucasevich', (2, 3, 3))

plot_binary_operation(fs1, fs2, 'union_max', (2, 3, 4))
plot_binary_operation(fs1, fs2, 'union_or', (2, 3, 5))
plot_binary_operation(fs1, fs2, 'union_lucasevich', (2, 3, 6), True)
