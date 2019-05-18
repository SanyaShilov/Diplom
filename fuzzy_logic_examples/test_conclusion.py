from matplotlib import pyplot as plt

from fuzzy_logic.fuzzy_base import FuzzyBase
from fuzzy_logic import membership_function
from fuzzy_logic.fuzzy_rule import FuzzyRule
from fuzzy_logic.fuzzy_set import *
from fuzzy_logic.logic_and_linguistics import *
from utils.range import Range


r_18_80 = Range(18, 80, h=0.5)
r_0_1 = Range(0, 1)

f_young = lambda x: 1 / (1 + ((x - 18) / 8) ** 8)
f_middle = membership_function.gaussian(40, 9)
f_old = lambda x: 1 / (1 + (abs(x - 90) / 28) ** 8)

f_very_old = f_very(f_old)

f_low = lambda x: lie_zade(x, 0.2)
f_high = lambda x: truth_zade(x, 0.2)

for func in [
    f_young, f_middle, f_old, f_very_old
]:
    fs = FuzzySet(r_18_80, func)
    plt.plot(*fs.plot())
plt.grid(True)
plt.show()

for func in [
    f_low, f_high
]:
    fs = FuzzySet(r_0_1, func)
    plt.plot(*fs.plot())
plt.grid(True)
plt.show()

input_28 = FuzzySet(r_18_80, membership_function.singleton(28))
input_40 = FuzzySet(r_18_80, membership_function.singleton(40))
input_young = FuzzySet(r_18_80, f_young)
input_middle = FuzzySet(r_18_80, f_middle)
input_old = FuzzySet(r_18_80, f_old)
input_very_old = FuzzySet(r_18_80, f_very_old)


base = FuzzyBase(
    [
        FuzzyRule(
            [FuzzySet(r_18_80, f_young)],
            FuzzySet(r_0_1, f_high)
        ),
        FuzzyRule(
            [FuzzySet(r_18_80, f_middle)],
            FuzzySet(r_0_1, f_low)
        ),
        FuzzyRule(
            [FuzzySet(r_18_80, f_very_old)],
            FuzzySet(r_0_1, f_high)
        ),
    ]
)

for input in [
    input_28, input_40, input_young, input_middle, input_old, input_very_old
]:
    print(base.evaluate([input]))
