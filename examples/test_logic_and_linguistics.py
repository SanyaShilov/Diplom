from matplotlib import pyplot as plt

from fuzzy_set import FuzzySet
from logic_and_linguistics import *
from range import Range


cold = lambda x: 1 / (1 + ((x - 12) / 6) ** 12)
comfortable = lambda x: 1 / (1 + ((x - 20) / 3) ** 8)
hot = lambda x: 1 / (1 + ((x - 33) / 8) ** 12)
not_very_cold = f_not(f_very(cold))
more_or_less_comfortable = f_more_or_less(comfortable)
very_hot = f_very(hot)

for func in [
    cold, comfortable, hot, not_very_cold, more_or_less_comfortable, very_hot
]:
    fs = FuzzySet(Range(12, 35), func)
    plt.plot(*fs.plot())
plt.grid(True)
plt.show()

for func in [
    truth_zade, lie_zade
]:
    fs = FuzzySet(BOOL_RANGE, func)
    plt.plot(*fs.plot())
plt.grid(True)
plt.show()

for func in [
    truth_baldwin, f_very(truth_baldwin),
    f_very(f_very(truth_baldwin)), f_more_or_less(truth_baldwin),
    lie_baldwin, f_very(lie_baldwin),
    f_very(f_very(lie_baldwin)), f_more_or_less(lie_baldwin),
]:
    fs = FuzzySet(BOOL_RANGE, func)
    plt.plot(*fs.plot())
plt.grid(True)
plt.show()

