from matplotlib import pyplot as plt

from fuzzy_logic.fuzzy_set import FuzzySet
from fuzzy_logic import membership_function
from utils.range import Range


fs1 = FuzzySet(Range(1, 4), membership_function.trapezoidal(1, 2, 3, 4))
fs2 = FuzzySet(Range(2, 8), membership_function.trapezoidal(2, 3, 4, 8))

result = FuzzySet.generalization_zade(fs1, fs2, f=lambda x1, x2: x1 * x2, k=10)
plt.plot(*result.plot())
plt.grid(True)
plt.show()

result = FuzzySet.generalization_alpha(fs1, fs2, f=lambda x1, x2: x1 * x2, k=10)
plt.plot(*result.plot())
plt.grid(True)
plt.show()
